// This is only a test not used and this code is incomplete

use serde::{Deserialize, Serialize};
use std::io::{self, Read, Write, Error, ErrorKind};
use std::process::{Command, Stdio};
use std::os::unix::net::UnixStream;
use std::path::Path;

const OCUPPED_WORKSPACES: &str = r#"hyprctl workspaces -j | jq -c 'sort_by(.id)' | jq -c -r '.[] | .id'"#;
const CURRENT_WORKSPACE: &str = r#"hyprctl activeworkspace -j | jq '.id'"#;
const WORKSPACE_NUMBER: usize = 10;

#[derive(Serialize, Deserialize)]
struct Workspace {
    id: String,
    active: i32,
    busy: i32,
}

fn run_command(command: &str) -> io::Result<String> {
    let output = Command::new("bash")
        .arg("-c")
        .arg(command)
        .output();

    match output {
        Ok(output) => {
            if output.status.success() {
                let result = String::from_utf8(output.stdout)
                    .map_err(|e| Error::new(ErrorKind::Other, format!("Failed to decode output: {}", e)))?;
                Ok(result.trim().to_string())
            } else {
                let stderr = String::from_utf8_lossy(&output.stderr);
                Err(Error::new(ErrorKind::Other, format!("Command failed with status {}: {}", output.status, stderr)))
            }
        }
        Err(e) => Err(e),
    }
}

fn get_ocupped_workspaces() -> io::Result<String> {
    run_command(OCUPPED_WORKSPACES)
}

fn get_active_workspace() -> io::Result<String> {
    run_command(CURRENT_WORKSPACE)
}

fn jdumps<T>(content: &T) -> io::Result<String>
where
    T: Serialize,
{
    serde_json::to_string(content).map_err(|e| io::Error::new(io::ErrorKind::Other, e))
}

fn eww_update(value: &Vec<Workspace>) -> io::Result<()> {
    let json_str = jdumps(value)?;
    println!("{}", json_str);
    run_command(&format!("eww update workspaces={}", json_str))?;
    Ok(())
}

fn mount_workspace() -> io::Result<()> {
    let mut workspaces = Vec::with_capacity(WORKSPACE_NUMBER);

    let wcurrent = get_active_workspace()?;
    let ocupped = get_ocupped_workspaces()?;

    let busy_workspaces_str = get_ocupped_workspaces()?;
    let busy_workspaces: Vec<usize> = busy_workspaces_str.lines().filter_map(|s| s.trim().parse().ok()).collect();

    for i in 1..=WORKSPACE_NUMBER {
        let id = i.to_string();
        let busyid = busy_workspaces.contains(&i);

        workspaces.push(Workspace {
            id: id.clone(),
            active: if wcurrent == id { 1 } else { 0 },
            busy: if busyid { 1 } else { 0 },
        });
    }

    eww_update(&workspaces)?;
    Ok(())
}

fn handler() -> io::Result<()> {
    let sp = Path::new("/tmp/hypr/")
        .join(std::env::var("HYPRLAND_INSTANCE_SIGNATURE").unwrap())
        .join(".socket2.sock");

    let mut s = UnixStream::connect(&sp)?;

    let mut buffer = [0; 1024];
    loop {
        let bytes_read = s.read(&mut buffer)?;
        let event = String::from_utf8_lossy(&buffer[..bytes_read]);

        if event.starts_with("workspace") || event.starts_with("focusedmon") {
            mount_workspace()?;
        }
        // Add more conditions for other events if needed
    }
}

fn main() {
    mount_workspace().unwrap();
    handler().unwrap();
}

