import { createClient } from 'https://esm.sh/@supabase/supabase-js@2';


const supabaseUrl = "https://sopoxavbgzasekfzjyrb.supabase.co";
const supabaseKey = "sb_publishable_cQfxPy_Jturhljr9sxlZbw__xTz7Z4Q";
const supabase = createClient(supabaseUrl, supabaseKey);

let kpi_data = []
let line_chart_data = []
let bar_chart_data = []
let notifications_data = []

async function getData() {
    const { data:kpi, error: kpi_error } = await supabase
    .from('vw_april_kpi')
    .select('*')

    const { data: complaints_per_month, error: complaints_per_month_Error } = await supabase
    .from("vw_complaints_per_month")
    .select("*");

    const { data: suburbs, error: suburbs_data_Error } = await supabase
    .from("vw_suburbs")
    .select("*");

    const { data: notifications, error: notifications_data_Error } = await supabase
    .from("vw_service_requests")
    .select("*");

    kpi_data = kpi
    line_chart_data = complaints_per_month
    bar_chart_data = suburbs
    notifications_data = notifications
    // if (error) {
    //     console.error("Error fetching data:", error)
    // } else {
    //     kpi_data = data
    // };
};

getData()

// KPI VALUES
getData().then(() => {
    console.log(kpi_data)
    const kpi = kpi_data[0];
    console.log(kpi)
    document.querySelector(".kpi:nth-child(1) .value").textContent = kpi.april_total_complaints;
    document.querySelector(".kpi:nth-child(2) .value").textContent = kpi.open_complaints;
    document.querySelector(".kpi:nth-child(3) .value").textContent = kpi.completed_complaints;
    document.querySelector(".kpi:nth-child(4) .value").textContent = kpi.avg_resolution_days;
});

// LINE CHART
getData().then(() => {
    console.log(line_chart_data)
    const labels = line_chart_data.map(row => new Date(row.day).toISOString().split("T")[0]); // x-axis labels
    const values = line_chart_data.map(row => row.total_complaints); // y-axis values

    const ctx = document.getElementById("kpiChart").getContext("2d");
    new Chart(ctx, {
        type: "line",
        data: {
            labels: labels,
            datasets: [{
            label: "Total Notifications",
            data: values,
            borderColor: "rgba(54, 162, 235, 0.8)",
            fill: false
            }]
        }
    });
});

// STATUS CHART
getData().then(() => {
    const ctx = document.getElementById("status-Chart").getContext("2d");
    new Chart(ctx, {
        type: "doughnut",   // chart type
        data: {
            labels: ["Open", "Resolved", "Notifications"], // categories
            datasets: [{
            label: "KPI Breakdown",
            data: [12, 19, 7], // replace with Supabase data
            backgroundColor: [
                "rgba(255, 99, 132, 0.6)",
                "rgba(54, 162, 235, 0.6)",
                "rgba(255, 206, 86, 0.6)"
            ],
            borderColor: [
                "rgba(255, 99, 132, 1)",
                "rgba(54, 162, 235, 1)",
                "rgba(255, 206, 86, 1)"
            ],
            borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            plugins: {
            legend: { position: "top" },
            title: { display: true, text: "KPI Donut Chart" }
            }
        }
    });
});

// BAR CHART
getData().then(() => {
    const labels = bar_chart_data.map(row => row.suburb); // y-axis values
    const values = bar_chart_data.map(row => row.total_complaints); // x-axis values

    const ctx = document.getElementById("bar-Chart").getContext("2d");
    new Chart(ctx, {
        type: "bar",   // still "bar"
        data: {
            labels: labels,
            datasets: [{
            label: "Notifications",
            data: values,
            backgroundColor: "rgba(54, 162, 235, 0.6)"
            }]
        },
        options: {
            indexAxis: "y",
            responsive: true,
            plugins: {
            legend: { display: false },
            title: { display: true, text: "Notifications by Suburb" }
            }
        }
    });
});


getData().then(() => {
    let currentPage = 0;
    const pageSize = 10;

    const tbody = document.querySelector("#notificationsTable tbody");
    tbody.innerHTML = "";

    const start = currentPage * pageSize;
    const end = start + pageSize;
    const pageData = notifications_data.slice(start, end);

    pageData.forEach(row => {
        const tr = document.createElement("tr");
        const createdDate = new Date(row.created_on_date);
        const createdText = createdDate.toLocaleDateString();

        const statusClass = row.status === "Open" ? "b-open" : "b-done";

        tr.innerHTML = `
            <td class="mono">${row.notification}</td>
            <td>${row.complaint_type}</td>
            <td class="muted">${row.suburb}</td>
            <td class="muted">${createdText}</td>
            <td class="right"><span class="badge ${statusClass}">${row.status}</span></td>
        `;

        tbody.appendChild(tr);
    });
});