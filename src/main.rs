mod app_logic;

use axum::{
    extract::Form,
    response::{Html, Redirect},
    routing::get,
    Router,
};
use askama::Template;
use serde::Deserialize;
use std::collections::BTreeMap;
use std::sync::Arc;
use tower_http::services::ServeDir;

use app_logic::{
    balance_sheet_config::get_position_names,
    calculator::calculate_selected_kpis,
    kpi_config::get_available_kpis,
    validators::validate_financial_data,
};

pub type AppState = Arc<app_logic::constants::AppState>;

#[derive(Template)]
#[template(path = "select_kpi.html")]
struct SelectKpiTemplate {
    categories: Vec<KpiCategory>,
}

struct KpiCategory {
    name: String,
    kpis: Vec<KpiItem>,
}

struct KpiItem {
    key: String,
    name: String,
    description: String,
}

#[derive(Template)]
#[template(path = "input.html")]
struct InputTemplate {
    assets: Vec<PositionInput>,
    liabilities_equity: Vec<PositionInput>,
    selected_kpis: Vec<String>,
}

struct PositionInput {
    pos: String,
    name: String,
    value: String,
}

#[derive(Template)]
#[template(path = "results.html")]
struct ResultsTemplate {
    results: Vec<KpiResultDisplay>,
    balance_check_valid: bool,
    balance_assets: f64,
    balance_liabilities_equity: f64,
}

struct KpiResultDisplay {
    name: String,
    value: String,
    status: String,
    message: String,
    is_ratio: bool,
    description: String,
}

#[tokio::main]
async fn main() {
    let state = Arc::new(app_logic::constants::AppState::new());

    let app = Router::new()
        .route("/", get(index))
        .route("/input", get(input_page).post(process_kpi_selection))
        .route("/calculate", get(show_results).post(calculate_kpis))
        .nest_service("/static", ServeDir::new("static"))
        .with_state(state);

    let listener = tokio::net::TcpListener::bind("127.0.0.1:5001").await.unwrap();
    println!("Server running on http://127.0.0.1:5001");
    axum::serve(listener, app).await.unwrap();
}

async fn index() -> Html<String> {
    let available_kpis = get_available_kpis();
    let mut categories: BTreeMap<String, Vec<KpiItem>> = BTreeMap::new();

    for (key, details) in available_kpis {
        let category = categories.entry(details.category_display.clone()).or_insert_with(Vec::new);
        category.push(KpiItem {
            key,
            name: details.name_display,
            description: details.description_short,
        });
    }

    let template = SelectKpiTemplate {
        categories: categories.into_iter().map(|(name, kpis)| KpiCategory { name, kpis }).collect(),
    };

    Html(template.render().unwrap())
}

async fn input_page(query: axum::extract::Query<BTreeMap<String, String>>) -> Html<String> {
    let position_names = get_position_names();
    
    let mut assets = Vec::new();
    let mut liabilities_equity = Vec::new();
    
    for i in 1..51 {
        let pos = i.to_string();
        if pos != "51" {
            if let Some(name) = position_names.get(&pos) {
                assets.push(PositionInput { pos: pos.clone(), name: name.clone(), value: "".to_string() });
            }
        }
    }
    
    for i in 52..101 {
        let pos = i.to_string();
        if let Some(name) = position_names.get(&pos) {
            liabilities_equity.push(PositionInput { pos: pos.clone(), name: name.clone(), value: "".to_string() });
        }
    }
    
    // Get selected KPIs from query params
    let selected_kpis: Vec<String> = query.get("kpis")
        .map(|s| s.split(',').map(|k| k.trim().to_string()).collect())
        .unwrap_or_else(|| vec![]);
    
    let template = InputTemplate { assets, liabilities_equity, selected_kpis };
    Html(template.render().unwrap())
}

async fn process_kpi_selection(Form(form): Form<KpiSelectionForm>) -> Redirect {
    let kpi_keys: Vec<String> = form.kpi_keys.clone();
    let kpi_list = kpi_keys.join(",");
    Redirect::to(&format!("/input?kpis={}", kpi_list))
}

async fn show_results() -> Html<String> {
    Html("<html><body><h1>Results</h1><p>KPI calculation results...</p></body></html>".to_string())
}

async fn calculate_kpis(Form(form): Form<BTreeMap<String, String>>) -> Html<String> {
    let available_kpis = get_available_kpis();
    let kpi_requirements = app_logic::kpi_requirements_logic::get_kpi_requirements();
    
    // Get selected KPIs from form (kpi_keys[])
    let selected_kpis: Vec<String> = form.get("kpi_keys[]")
        .map(|s| vec![s.clone()])
        .unwrap_or_else(|| vec![]);
    
    // Get required positions for validation
    let mut required_positions = Vec::new();
    for kpi_key in &selected_kpis {
        if let Some(reqs) = kpi_requirements.get(kpi_key) {
            for pos in reqs {
                if !required_positions.contains(pos) {
                    required_positions.push(pos.clone());
                }
            }
        }
    }
    
    // Validate financial data
    let (validated_data, errors) = validate_financial_data(&form, &required_positions);
    
    if !errors.is_empty() {
        return Html("<html><body><h1>Error</h1><p>Validation failed</p></body></html>".to_string());
    }
    
    // Calculate KPIs
    let results = calculate_selected_kpis(&validated_data, &selected_kpis);
    
    // Convert to display format
    let mut display_results = Vec::new();
    for (key, result) in &results {
        if let Some(kpi_details) = available_kpis.get(key) {
            let value_str = result.value.map_or("".to_string(), |v| format!("{:.2}", v));
            display_results.push(KpiResultDisplay {
                name: kpi_details.name_display.clone(),
                value: value_str,
                status: result.status.clone(),
                message: result.message.clone(),
                is_ratio: kpi_details.is_ratio,
                description: kpi_details.description_short.clone(),
            });
        }
    }
    
    let template = ResultsTemplate {
        results: display_results,
        balance_check_valid: true,
        balance_assets: 0.0,
        balance_liabilities_equity: 0.0,
    };
    
    Html(template.render().unwrap())
}

#[derive(Debug, Deserialize)]
pub struct KpiSelectionForm {
    kpi_keys: Vec<String>,
}
