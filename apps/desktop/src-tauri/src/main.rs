#![cfg_attr(not(debug_assertions), windows_subsystem = "windows")]

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

fn main() {
    tauri::Builder::default()
        .invoke_handler(tauri::generate_handler![list_providers])
        .run(tauri::generate_context!())
        .expect("error while running GEO Agent desktop app");
}
