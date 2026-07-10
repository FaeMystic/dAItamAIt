async function analyze() {

    const ticker = document.getElementById("ticker").value;

    const response = await fetch("/analyze?ticker=" + ticker);

    const data = await response.json();

    document.getElementById("results").innerHTML = `

    <div class="signal">
        ${data.signal}
    </div>

    <div class="grid">

        <div class="card">

            <h2>Company</h2>

            <div class="metric"><b>Name:</b> ${data.company_name}</div>
            <div class="metric"><b>Sector:</b> ${data.sector}</div>
            <div class="metric"><b>Industry:</b> ${data.industry}</div>
            <div class="metric"><b>Market Cap:</b> ${data.market_cap}</div>

        </div>

        <div class="card">

            <h2>Market Overview</h2>

            <div class="metric"><b>Price:</b> $${data.price}</div>
            <div class="metric"><b>Trend:</b> ${data.trend}</div>
            <div class="metric"><b>Confidence:</b> ${data.confidence}</div>
            <div class="metric"><b>Trade Score:</b> ${data.trade_score}</div>

            <div class="score-bar">
                <div
                    class="score-fill"
                    style="width:${data.trend_strength}%;">
                    ${data.trend_strength}%
                </div>
            </div>

        </div>

        <div class="card">

            <h2>Trade Plan</h2>

            <div class="metric">Entry: $${data.entry_price}</div>
            <div class="metric">Stop: $${data.stop_loss}</div>
            <div class="metric">Target: $${data.take_profit}</div>
            <div class="metric">Risk / Reward: ${data.risk_reward}</div>

        </div>

        <div class="card">

            <h2>Multi-Timeframe</h2>

            <div class="metric">${data.weekly_trend}</div>
            <div class="metric">${data.daily_trend}</div>
            <div class="metric">${data.hourly_trend}</div>
            <div class="metric">Alignment: ${data.alignment_score}</div>

        </div>

        <div class="card">

            <h2>Technical Indicators</h2>

            <div class="metric">${data.ema_status}</div>
            <div class="metric">${data.macd_status}</div>
            <div class="metric">${data.rsi_status}</div>
            <div class="metric">${data.atr_status}</div>

        </div>

        <div class="card">

            <h2>AI Analysis</h2>

            <p>${data.reason}</p>

        </div>

        <div class="card" style="grid-column:1/-1;">

            <h2>Price Chart</h2>

            <canvas id="priceChart"></canvas>

        </div>

    </div>
    `;

    const ctx = document.getElementById("priceChart");

    new Chart(ctx, {

        type: "line",

        data: {

            labels: data.chart_labels,

            datasets: [

                {
                    label: "Price",
                    data: data.chart_prices
                },

                {
                    label: "EMA20",
                    data: data.chart_ema20
                },

                {
                    label: "EMA50",
                    data: data.chart_ema50
                }

            ]

        },

        options: {

            responsive: true,

            plugins: {

                legend: {

                    labels: {

                        color: "white"

                    }

                }

            },

            scales: {

                x: {

                    ticks: {

                        color: "white"

                    }

                },

                y: {

                    ticks: {

                        color: "white"

                    }

                }

            }

        }

    });

}
