// Simple bucket planner
(function(){
  const STORAGE_KEY = 'bucket_planner_v1'

  const els = {
    currentBalance: document.getElementById('currentBalance'),
    mainIncrease: document.getElementById('mainIncrease'),
    date1: document.getElementById('date1'),
    date2: document.getElementById('date2'),
    months: document.getElementById('months'),
    applyBtn: document.getElementById('applyBtn'),
    saveBtn: document.getElementById('saveBtn'),
    resetBtn: document.getElementById('resetBtn'),
    addBucket: document.getElementById('addBucket'),
    buckets: document.getElementById('buckets'),
    summary: document.getElementById('summary')
  }

  let state = load() || {
    currentBalance: 1000,
    mainIncrease: 200,
    date1: 1,
    date2: 15,
    buckets: [
      {id: id(), name:'Emergency', pct:30, amount:0, periodic:50, goal:1000},
      {id: id(), name:'Vacation', pct:20, amount:0, periodic:30, goal:600},
      {id: id(), name:'Invest', pct:30, amount:0, periodic:50, goal:2000}
    ]
  }

  function id(){return Math.random().toString(36).slice(2,9)}

  function save(){localStorage.setItem(STORAGE_KEY, JSON.stringify(state))}
  function load(){try{return JSON.parse(localStorage.getItem(STORAGE_KEY))}catch(e){return null}}

  function renderBuckets(){
    els.buckets.innerHTML = ''
    state.buckets.forEach(b=>{
      const div = document.createElement('div'); div.className='bucket card';
      div.innerHTML = `
        <input data-id="${b.id}" class="name" value="${escapeHtml(b.name)}">
        <input data-id="${b.id}" class="pct" type="number" min="0" max="100" value="${b.pct}"> %
        <input data-id="${b.id}" class="periodic" type="number" step="0.01" value="${b.periodic}"> periodic
        <input data-id="${b.id}" class="goal" type="number" step="0.01" value="${b.goal}"> goal
        <button data-id="${b.id}" class="remove">Remove</button>
        <div class="canvas-wrap"><canvas id="c_${b.id}"></canvas></div>
      `
      els.buckets.appendChild(div)
    })
    attachBucketHandlers()
  }

  function escapeHtml(s){return String(s).replace(/[&<>"]/g, c=>({ '&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;' }[c]))}

  function attachBucketHandlers(){
    document.querySelectorAll('#buckets .remove').forEach(btn=>btn.onclick = e=>{ const id=e.target.dataset.id; state.buckets = state.buckets.filter(b=>b.id!==id); render(); })
    document.querySelectorAll('#buckets .name').forEach(inp=>inp.oninput = e=>{ const b = state.buckets.find(x=>x.id===e.target.dataset.id); if(b) b.name = e.target.value })
    document.querySelectorAll('#buckets .pct').forEach(inp=>inp.oninput = e=>{ const b = state.buckets.find(x=>x.id===e.target.dataset.id); if(b) b.pct = Number(e.target.value) })
    document.querySelectorAll('#buckets .periodic').forEach(inp=>inp.oninput = e=>{ const b = state.buckets.find(x=>x.id===e.target.dataset.id); if(b) b.periodic = Number(e.target.value) })
    document.querySelectorAll('#buckets .goal').forEach(inp=>inp.oninput = e=>{ const b = state.buckets.find(x=>x.id===e.target.dataset.id); if(b) b.goal = Number(e.target.value) })
  }

  function applySimulation(){
    // copy state
    let balance = Number(els.currentBalance.value)||0
    const mainInc = Number(els.mainIncrease.value)||0
    const date1 = Number(els.date1.value)||1
    const date2 = Number(els.date2.value)||15
    const months = Number(els.months.value)||0

    // initial allocation by percentage
    state.buckets.forEach(b=>{
      b.amount = Math.round((b.pct/100) * balance * 100)/100
    })

    // unallocated
    let allocated = state.buckets.reduce((s,b)=>s+b.amount,0)
    let remaining = Math.round((balance - allocated)*100)/100

    // simulate twice-monthly increases for 'months' months
    for(let m=0;m<months;m++){
      // two events per month
      balance += mainInc
      state.buckets.forEach(b=> b.amount += b.periodic )
    }

    renderSummary(balance, remaining)
    renderCharts()
  }

  function renderSummary(balance, remaining){
    els.summary.innerHTML = ''
    const totalBucket = state.buckets.reduce((s,b)=>s + b.amount,0)
    const div = document.createElement('div')
    div.innerHTML = `
      <p><strong>Bank balance after simulation:</strong> ${format(balance)}</p>
      <p><strong>Total in buckets:</strong> ${format(totalBucket)}</p>
      <p><strong>Unallocated / cash remaining:</strong> ${format(balance - totalBucket)}</p>
    `
    els.summary.appendChild(div)
    // detailed per-bucket
    state.buckets.forEach(b=>{
      const p = document.createElement('p')
      p.textContent = `${b.name}: ${format(b.amount)} / ${format(b.goal)} (periodic +${format(b.periodic)})`
      els.summary.appendChild(p)
    })
  }

  function format(n){return new Intl.NumberFormat(undefined,{style:'currency',currency:'USD',maximumFractionDigits:2}).format(Number(n))}

  function renderCharts(){
    state.buckets.forEach(b=>{
      const canvas = document.getElementById('c_'+b.id)
      if(!canvas) return
      const completed = Math.min(b.amount, b.goal)
      const remaining = Math.max(b.goal - b.amount, 0)
      // destroy existing chart instance to avoid duplicates
      if(canvas._chart) canvas._chart.destroy()
      canvas._chart = new Chart(canvas.getContext('2d'),{
        type:'doughnut',
        data:{datasets:[{data:[completed,remaining],backgroundColor:['#2b6cb0','#e6e9ef']}]},
        options:{plugins:{legend:{display:false},tooltip:{callbacks:{label:(ctx)=>ctx.label?ctx.label:''}}},cutout:'60%'}
      })
    })
  }

  function addBucket(){ state.buckets.push({id:id(),name:'New',pct:0,amount:0,periodic:0,goal:100}); render(); }

  function render(){
    // update inputs from state
    els.currentBalance.value = state.currentBalance
    els.mainIncrease.value = state.mainIncrease
    els.date1.value = state.date1
    els.date2.value = state.date2
    renderBuckets()
    renderCharts()
    save()
  }

  // event wiring
  els.addBucket.onclick = addBucket
  els.applyBtn.onclick = ()=>{ // sync state from form then simulate
    state.currentBalance = Number(els.currentBalance.value)||0
    state.mainIncrease = Number(els.mainIncrease.value)||0
    state.date1 = Number(els.date1.value)||1
    state.date2 = Number(els.date2.value)||15
    applySimulation()
  }
  els.saveBtn.onclick = ()=>{ state.currentBalance = Number(els.currentBalance.value)||0; save(); alert('Saved') }
  els.resetBtn.onclick = ()=>{ if(confirm('Reset to defaults?')){ localStorage.removeItem(STORAGE_KEY); location.reload() } }

  // initial render
  render()
})()

