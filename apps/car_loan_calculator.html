<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>Car Loan Calculator</title>
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap" rel="stylesheet">
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.1/dist/chart.umd.min.js"></script>
<style>
  :root{ --accent:#0ea5e9; --card:#ffffff; --muted:#6b7280; }
  *{box-sizing:border-box}
  body{margin:0;font-family:Inter,system-ui,-apple-system,Segoe UI,Roboto,Helvetica,Arial,sans-serif;background:#f4f7fb;color:#0f172a;}
  .wrap{max-width:1000px;margin:20px auto;padding:0 16px}
  h1{margin:0 0 6px 0;color:#0f172a;font-size:28px;font-weight:800}
  .subtitle{color:#0b5b78;margin-bottom:10px;font-weight:600}
  .grid{display:grid;grid-template-columns:1.2fr .8fr;gap:20px}
  .card{background:var(--card);border-radius:14px;box-shadow:0 6px 20px rgba(2,8,23,.06);padding:18px}
  .row{display:grid;grid-template-columns:190px 1fr;align-items:center;gap:8px;margin:8px 0}
  input[type="number"], select{width:100%;padding:10px 12px;border:1px solid #e5e7eb;border-radius:10px;font-size:14px}
  .flex{display:flex;gap:8px;align-items:center;flex-wrap:wrap}
  .muted{color:var(--muted)}
  .btn{background:var(--accent);color:white;border:0;border-radius:10px;padding:10px 14px;font-weight:700;cursor:pointer}
  .chartWrap{height:260px;margin-top:8px}
  .sectionTitle{font-weight:800;margin:4px 0 8px}
  .summaryNum{font-size:28px;font-weight:800}
  .small{font-size:12px;color:var(--muted)}
  table{width:100%;border-collapse:collapse;font-size:13px}
  th, td{padding:8px;border-bottom:1px solid #eef2f7;text-align:right}
  th:first-child, td:first-child{text-align:left}
  @media (max-width: 950px){ .grid{grid-template-columns:1fr} }
</style>
</head>
<body>
  <div class="wrap">
    <h1>Car Loan Calculator</h1>
    <div class="subtitle">Estimate your monthly payment and total cost</div>

    <div class="grid">
      <!-- LEFT: inputs + chart -->
      <div class="card">
        <div class="row">
          <div>Vehicle Price:</div>
          <div class="flex">
            <input id="price" type="number" step="0.01" value="45000" />
            <span class="muted">$</span>
          </div>
        </div>

        <div class="row">
          <div>Down Payment:</div>
          <div class="flex">
            <input id="down" type="number" step="0.01" value="5000" />
            <span class="muted">$</span>
          </div>
        </div>

        <div class="row">
          <div>Trade-in Value:</div>
          <div class="flex">
            <input id="tradein" type="number" step="0.01" value="0" />
            <span class="muted">$</span>
          </div>
        </div>

        <div class="row">
          <div>Sales Tax:</div>
          <div class="flex">
            <input id="taxPct" type="number" step="0.01" value="7" />
            <span class="muted">%</span>
          </div>
        </div>

        <div class="row">
          <div>Fees (title/registration, etc.):</div>
          <div class="flex">
            <input id="fees" type="number" step="0.01" value="500" />
            <span class="muted">$</span>
          </div>
        </div>

        <div class="row">
          <div>APR (Interest Rate):</div>
          <div class="flex">
            <input id="apr" type="number" step="0.01" value="5.5" />
            <span class="muted">%</span>
          </div>
        </div>

        <div class="row">
          <div>Loan Term:</div>
          <div class="flex">
            <input id="termMonths" type="number" value="60" />
            <span class="muted">months</span>
          </div>
        </div>

        <div class="row">
          <div>Start Date:</div>
          <div class="flex">
            <select id="startMonth"></select>
            <input id="startYear" type="number" />
          </div>
        </div>

        <div class="row">
          <div>Amount Financed:</div>
          <div class="flex">
            <input id="financed" type="number" step="0.01" value="0" readonly />
            <span class="muted">$</span>
          </div>
        </div>

        <div class="flex" style="margin-top:10px">
          <button class="btn" id="calcBtn">Calculate</button>
        </div>

        <div class="chartWrap"><canvas id="loanChart"></canvas></div>
      </div>

      <!-- RIGHT: summary -->
      <div class="card">
        <div class="sectionTitle">Loan Summary</div>
        <div class="summaryNum" id="monthlyPay">$0.00</div>
        <div class="small">Estimated Monthly Payment</div>

        <div class="row" style="margin-top:6px">
          <div>Amount Financed</div><div id="financedLbl">$0.00</div>
        </div>
        <div class="row">
          <div>Total Interest Paid</div><div id="totalInterestLbl">$0.00</div>
        </div>
        <div class="row">
          <div>Total of Payments</div><div id="totalPaymentsLbl">$0.00</div>
        </div>
        <div class="row">
          <div>Loan Pay-off Date</div><div id="payoffLbl">—</div>
        </div>
      </div>
    </div>

    <div id="amort" class="card" style="margin-top:20px">
      <div class="sectionTitle">Amortization Schedule</div>
      <table id="amortTable">
        <thead>
          <tr><th>#</th><th>Date</th><th>Principal</th><th>Interest</th><th>Total</th><th>Balance</th></tr>
        </thead>
        <tbody></tbody>
      </table>
      <div class="small muted" id="amortNote"></div>
    </div>
  </div>

<script>
  // ---------- helpers ----------
  const months = [["Jan",1],["Feb",2],["Mar",3],["Apr",4],["May",5],["Jun",6],["Jul",7],["Aug",8],["Sep",9],["Oct",10],["Nov",11],["Dec",12]];
  const q = id => document.getElementById(id);
  function fmt(x){ return "$"+Number(x||0).toLocaleString(undefined,{minimumFractionDigits:2,maximumFractionDigits:2}); }
  function addMonths(y,m,add){ const y2 = y + Math.floor((m-1+add)/12); const m2 = ((m-1+add)%12)+1; return [y2,m2]; }
  function payoffString(y,m,n){ const [yy,mm] = addMonths(y,m,n-1); const d = new Date(yy,mm-1,1); return d.toLocaleString('en-US',{month:'short', year:'numeric'}); }
  function pmt(principal, annualRatePct, nMonths){
    const r = (annualRatePct/100)/12;
    if(nMonths<=0) return 0;
    if(Math.abs(r) < 1e-12) return principal / nMonths;
    return principal * (r * Math.pow(1+r, nMonths)) / (Math.pow(1+r, nMonths) - 1);
  }

  // Init start date
  (function initStart(){
    const sm = q("startMonth");
    months.forEach(([label,m])=>{
      const o = document.createElement("option"); o.value=m; o.textContent=label; sm.appendChild(o);
    });
    const now = new Date();
    q("startMonth").value = now.getMonth()+1;
    q("startYear").value  = now.getFullYear();
  })();

  let chart;
  function renderChart(labels, principalArr, interestArr, balanceArr){
    const ctx = q("loanChart");
    if(chart) chart.destroy();
    chart = new Chart(ctx, {
      data:{
        labels: labels,
        datasets:[
          {type:'bar', label:'Principal', data:principalArr, stack:'s0'},
          {type:'bar', label:'Interest',  data:interestArr,  stack:'s0'},
          {type:'line',label:'Balance', data:balanceArr, yAxisID:'y1'}
        ]
      },
      options:{
        responsive:true, interaction:{mode:'index',intersect:false},
        plugins:{ legend:{position:'top'} },
        scales:{
          y:{ beginAtZero:true, ticks:{ callback:v=>"$"+v.toLocaleString() } },
          y1:{ position:'right', grid:{drawOnChartArea:false}, ticks:{ callback:v=>"$"+v.toLocaleString() } }
        }
      }
    });
  }

  function calc(){
    const price   = parseFloat(q("price").value||0);
    const down    = parseFloat(q("down").value||0);
    const tradein = parseFloat(q("tradein").value||0);
    const taxPct  = parseFloat(q("taxPct").value||0);
    const fees    = parseFloat(q("fees").value||0);
    const apr     = parseFloat(q("apr").value||0);
    const n       = parseInt(q("termMonths").value||60);
    const startMonth = parseInt(q("startMonth").value||1);
    const startYear  = parseInt(q("startYear").value||new Date().getFullYear());

    // Assumption: sales tax is applied to (price - trade-in). Down payment does NOT reduce taxable base (common in many states).
    const taxableBase = Math.max(price - tradein, 0);
    const taxAmt = taxableBase * (taxPct/100);
    const financed = Math.max(taxableBase + taxAmt + fees - down, 0);

    q("financed").value = financed.toFixed(2);
    q("financedLbl").textContent = fmt(financed);

    const pay = pmt(financed, apr, n);

    // Build amortization
    let bal = financed;
    const rows = [];
    let totInterest = 0;
    for(let i=1;i<=n;i++){
      const r = (apr/100)/12;
      const interest = bal * r;
      let principal = pay - interest;
      if (principal > bal){ principal = bal; }  // last payment
      bal -= principal;

      const d = new Date(startYear, startMonth-1 + (i-1), 1);
      rows.push({
        idx:i,
        date:d.toLocaleString('en-US',{month:'short', year:'numeric'}),
        principal, interest, total:principal+interest, balance:Math.max(bal,0)
      });
      totInterest += interest;
    }

    // Summary
    q("monthlyPay").textContent = fmt(pay);
    q("totalInterestLbl").textContent = fmt(totInterest);
    q("totalPaymentsLbl").textContent = fmt(rows.reduce((s,r)=>s+r.total,0));
    q("payoffLbl").textContent = payoffString(startYear, startMonth, n);

    // Table
    const tbody = document.querySelector("#amortTable tbody");
    tbody.innerHTML = "";
    const maxRows = 360; // performance cap
    rows.slice(0,maxRows).forEach(r=>{
      const tr = document.createElement("tr");
      tr.innerHTML = `<td>${r.idx}</td><td>${r.date}</td>
        <td>${fmt(r.principal)}</td><td>${fmt(r.interest)}</td>
        <td>${fmt(r.total)}</td><td>${fmt(r.balance)}</td>`;
      tbody.appendChild(tr);
    });
    document.getElementById("amortNote").textContent = rows.length>maxRows ? "Showing first 360 rows for speed." : "";

    // Chart (downsample to ~25 points)
    const labels=[], princ=[], intr=[], balArr=[];
    const step = Math.max(1, Math.floor(rows.length/25)) || 1;
    for(let i=0;i<rows.length;i+=step){
      const chunk = rows.slice(i,i+step);
      labels.push(chunk[chunk.length-1].date);
      princ.push(chunk.reduce((s,x)=>s+x.principal,0));
      intr.push(chunk.reduce((s,x)=>s+x.interest,0));
      balArr.push(chunk[chunk.length-1].balance);
    }
    renderChart(labels, princ, intr, balArr);
  }

  // events
  ["price","down","tradein","taxPct","fees","apr","termMonths","startMonth","startYear"]
    .forEach(id => q(id).addEventListener("change", calc));
  q("calcBtn").addEventListener("click", calc);
  window.addEventListener("load", calc);
</script>
</body>
</html>
