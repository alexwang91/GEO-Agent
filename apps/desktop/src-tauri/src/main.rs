#![cfg_attr(not(debug_assertions), windows_subsystem = "windows")]

use std::process::Command;

#[derive(serde::Serialize)]
struct FixtureAuditPackage {
    status: String,
    fixture_path: String,
    output_dir: String,
    manifest_path: String,
    report_json_path: String,
    report_markdown_path: String,
    data_file_path: String,
}

#[tauri::command]
fn list_providers() -> Vec<&'static str> {
    vec![
        "OpenAI-compatible",
        "Perplexity",
        "Gemini",
        "Crawl4AI",
        "Firecrawl",
        "Google Search Console",
        "Manual Import",
    ]
}

#[tauri::command]
fn run_fixture_audit(fixture_path: String, output_dir: String) -> Result<FixtureAuditPackage, String> {
    let status = Command::new("python")
        .args(["-m", "geo_agent.cli", "audit", fixture_path.as_str(), "--out", output_dir.as_str()])
        .status()
        .map_err(|error| format!("Unable to start fixture audit command: {error}"))?;

    if !status.success() {
        return Err(format!("Fixture audit command failed with status: {status}"));
    }

    Ok(FixtureAuditPackage {
        status: "completed".to_string(),
        fixture_path: fixture_path.clone(),
        output_dir: output_dir.clone(),
        manifest_path: format!("{output_dir}/manifest.json"),
        report_json_path: format!("{output_dir}/report.json"),
        report_markdown_path: format!("{output_dir}/report.md"),
        data_file_path: format!("{output_dir}/audit.sqlite"),
    })
}

fn main() {
    tauri::Builder::default()
        .invoke_handler(tauri::generate_handler![list_providers, run_fixture_audit])
        .run(tauri::generate_context!())
        .expect("error while running GEO Agent desktop app");
}