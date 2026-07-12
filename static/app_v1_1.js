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

    	<h2>${data.company_name}</h2>

    	<div class="metric"><b>Ticker:</b> ${data.ticker}</div>

    	<div class="metric"><b>CEO:</b> ${data.ceo}</div>

    	<div class="metric"><b>Sector:</b> ${data.sector}</div>

    	<div class="metric"><b>Industry:</b> ${data.industry}</div>

    	<div class="metric"><b>Employees:</b> ${data.employees.toLocaleString()}</div>

    	<div class="metric"><b>Headquarters:</b> ${data.city}, ${data.country}</div>

    	<div class="metric"><b>Market Cap:</b> ${data.market_cap}</div>

    	<div class="metric">
        	<b>Website:</b>
        	<a href="${data.website}" target="_blank">${data.website}</a>
    </div>
	<p style="margin-top:20px; line-height:1.5;">
    	 ${data.summary.substring(0,350)}...
	    </p>

        </div>

        <div class="card">

            <h2>Market Overview</h2>

            <div class="metric"><b>Price:</b> $${data.price}</div>
	<div class="metric">
    	    <b>Today's Change:</b>
    	    <span style="color:${data.change >= 0 ? '#22c55e' : '#ef4444'}">
       		 ${data.change >= 0 ? '+' : ''}${data.change}
                 (${data.percent_change}%)
    		 </span>
	</div>

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
	    <div style="height:400px; width:100%;">
    	    <canvas id="priceChart"></canvas>
	</div>
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
    	data: data.chart_prices,
    	borderColor: "#00ff66",
    	backgroundColor: "transparent",
    	borderWidth: 3,
    	pointRadius: 0,
    	tension: 0.2
},
{
    	label: "EMA20",
    	data: data.chart_ema20,
    	borderColor: "#ffd700",
    	backgroundColor: "transparent",
    	borderWidth: 2,
    	pointRadius: 0,
    	tension: 0.2
},
{
	label: "EMA50",
    	data: data.chart_ema50,
    	borderColor: "#00bfff",
    	backgroundColor: "transparent",
    	borderWidth: 2,
    	pointRadius: 0,
    	tension: 0.2
}
]
        },

        options: {

            responsive: true,
	    maintainAspectRatio: false,

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
