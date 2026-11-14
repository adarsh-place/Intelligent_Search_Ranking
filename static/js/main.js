/**
 * Intelligent Search Ranking Frontend Controller
 * MFCS Project - Web Graphs, Markov Chains & IR
 */

// Application State
let activeTab = 'search';
let searchViewMode = 'unified'; // 'unified' or 'compare'
let selectedDocId = null;
let networkInstance = null;
let networkData = null;
let graphCache = null;
let surferChartInstance = null;
let dampingChartInstance = null;
let currentSearchData = null;
let currentTheme = localStorage.getItem('theme') || 'light';

// Initialization on DOM Loaded
document.addEventListener('DOMContentLoaded', () => {
  initTheme();
  initNetworkGraph();
  triggerSearch();
  loadDampingExperiment();
  populateNodeSelects();
});

// --------------------------------------------------------------------------
// THEME MANAGEMENT (LIGHT / DARK TOGGLE)
// --------------------------------------------------------------------------

function initTheme() {
  applyTheme(currentTheme);
}

function toggleTheme() {
  const newTheme = (currentTheme === 'dark') ? 'light' : 'dark';
  applyTheme(newTheme);
}

function applyTheme(theme) {
  currentTheme = theme;
  localStorage.setItem('theme', theme);

  const html = document.documentElement;
  const sunIcon = document.getElementById('theme-icon-sun');
  const moonIcon = document.getElementById('theme-icon-moon');

  if (theme === 'dark') {
    html.classList.add('dark');
    html.classList.remove('light');
    if (sunIcon) sunIcon.classList.remove('hidden');
    if (moonIcon) moonIcon.classList.add('hidden');
  } else {
    html.classList.remove('dark');
    html.classList.add('light');
    if (sunIcon) sunIcon.classList.add('hidden');
    if (moonIcon) moonIcon.classList.remove('hidden');
  }

  // Update Vis.js network node font colors & edge colors
  if (networkInstance) {
    const isDark = (theme === 'dark');
    networkInstance.setOptions({
      nodes: {
        font: {
          color: isDark ? '#F8FAFC' : '#0F172A',
          bold: { color: isDark ? '#FFFFFF' : '#000000' }
        }
      },
      edges: {
        color: {
          color: isDark ? '#64748B' : '#94A3B8',
          highlight: '#6366F1'
        }
      }
    });
  }

  // Re-render charts with updated theme colors if they exist
  if (surferChartInstance) {
    updateChartTheme(surferChartInstance);
  }
  if (dampingChartInstance) {
    updateChartTheme(dampingChartInstance);
  }
}

function updateChartTheme(chart) {
  const isDark = (currentTheme === 'dark');
  const textColor = isDark ? '#94A3B8' : '#475569';
  const gridColor = isDark ? 'rgba(51, 65, 85, 0.4)' : 'rgba(226, 232, 240, 0.8)';
  const legendColor = isDark ? '#E2E8F0' : '#1E293B';

  if (chart.options.plugins && chart.options.plugins.legend) {
    chart.options.plugins.legend.labels.color = legendColor;
  }

  if (chart.options.scales) {
    Object.keys(chart.options.scales).forEach(scaleKey => {
      const scale = chart.options.scales[scaleKey];
      if (scale.ticks) scale.ticks.color = textColor;
      if (scale.grid) scale.grid.color = gridColor;
      if (scale.title) scale.title.color = isDark ? '#C7D2FE' : '#3730A3';
    });
  }
  chart.update();
}

// --------------------------------------------------------------------------
// TAB NAVIGATION
// --------------------------------------------------------------------------

function switchTab(tabId) {
  activeTab = tabId;
  document.querySelectorAll('.tab-btn').forEach(btn => {
    btn.classList.remove('active');
    btn.classList.add('text-slate-600', 'dark:text-slate-400');
  });
  document.querySelectorAll('.tab-view').forEach(view => view.classList.add('hidden'));

  const activeBtn = document.getElementById(`tab-${tabId}-btn`);
  if (activeBtn) {
    activeBtn.classList.add('active');
    activeBtn.classList.remove('text-slate-600', 'dark:text-slate-400');
  }

  const targetView = document.getElementById(`view-${tabId}`);
  if (targetView) targetView.classList.remove('hidden');

  if (tabId === 'graph') {
    setTimeout(() => {
      if (networkInstance) {
        networkInstance.fit();
      } else {
        loadGraphData();
      }
    }, 120);
  }
}

// --------------------------------------------------------------------------
// 1. SEARCH & HYBRID RANKING MODULE
// --------------------------------------------------------------------------

function setQuery(queryText) {
  document.getElementById('search-input').value = queryText;
}

function updateAlphaSlider(val) {
  const floatVal = parseFloat(val);
  document.getElementById('alpha-val').innerText = floatVal.toFixed(2);
  document.getElementById('col-hybrid-badge').innerText = `α = ${floatVal.toFixed(2)}`;
  triggerSearch();
}

function updateDampingSlider(val) {
  const floatVal = parseFloat(val);
  document.getElementById('damping-val').innerText = floatVal.toFixed(2);
  triggerSearch();
  if (activeTab === 'graph') loadGraphData();
}

async function triggerSearch() {
  const query = document.getElementById('search-input').value.trim();
  const alpha = parseFloat(document.getElementById('alpha-slider').value);
  const damping = parseFloat(document.getElementById('damping-slider').value);
  const filterUnmatched = document.getElementById('filter-unmatched-chk').checked;

  try {
    const response = await fetch('/api/search', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        query: query,
        alpha: alpha,
        damping: damping,
        filter_unmatched: filterUnmatched
      })
    });
    const data = await response.json();
    currentSearchData = data;
    renderSearchResults(data);
    updateMetricsRibbon(data);
  } catch (err) {
    console.error('Search request failed:', err);
  }
}

function setSearchViewMode(mode) {
  searchViewMode = mode;
  const unifiedBtn = document.getElementById('view-mode-unified-btn');
  const compareBtn = document.getElementById('view-mode-compare-btn');
  const unifiedView = document.getElementById('search-unified-view');
  const compareView = document.getElementById('search-compare-view');

  if (mode === 'unified') {
    if (unifiedBtn) {
      unifiedBtn.classList.add('active');
      unifiedBtn.classList.remove('text-slate-600', 'dark:text-slate-400');
    }
    if (compareBtn) {
      compareBtn.classList.remove('active');
      compareBtn.classList.add('text-slate-600', 'dark:text-slate-400');
    }
    if (unifiedView) unifiedView.classList.remove('hidden');
    if (compareView) compareView.classList.add('hidden');
  } else {
    if (compareBtn) {
      compareBtn.classList.add('active');
      compareBtn.classList.remove('text-slate-600', 'dark:text-slate-400');
    }
    if (unifiedBtn) {
      unifiedBtn.classList.remove('active');
      unifiedBtn.classList.add('text-slate-600', 'dark:text-slate-400');
    }
    if (compareView) compareView.classList.remove('hidden');
    if (unifiedView) unifiedView.classList.add('hidden');
  }
}

function updateMetricsRibbon(data) {
  const candElem = document.getElementById('metric-candidates');
  const rhoTfElem = document.getElementById('metric-rho-tfidf');
  const rhoPrElem = document.getElementById('metric-rho-pr');
  const iterElem = document.getElementById('metric-iterations');

  if (candElem) candElem.innerText = data.num_candidates;
  if (rhoTfElem) rhoTfElem.innerText = (data.correlations.spearman_keyword_vs_combined).toFixed(3);
  if (rhoPrElem) rhoPrElem.innerText = (data.correlations.spearman_pagerank_vs_combined).toFixed(3);
  
  const iters = data.pagerank_metadata?.iterations || '--';
  if (iterElem) iterElem.innerText = `${iters}`;
}

function renderSearchResults(data) {
  // 1. Render Unified Stream
  renderUnifiedResults(data.combined_ranking, data.alpha);

  // 2. Render 3-Way Compare Columns
  renderColumn(document.getElementById('col-keyword-results'), data.keyword_only_ranking, 'keyword');
  renderColumn(document.getElementById('col-pagerank-results'), data.pagerank_only_ranking, 'pagerank');
  renderColumn(document.getElementById('col-hybrid-results'), data.combined_ranking, 'hybrid');
}

function renderUnifiedResults(records, alpha) {
  const container = document.getElementById('unified-results-container');
  if (!container) return;

  if (!records || records.length === 0) {
    container.innerHTML = `
      <div class="p-8 text-center bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl text-slate-400 text-xs">
        No documents matched your query filter. Try broadening your keywords or unchecking "Filter unmatched".
      </div>`;
    renderDocumentInspector(null);
    return;
  }

  // Ensure an item is selected
  if (!selectedDocId || !records.some(r => r.id === selectedDocId)) {
    selectedDocId = records[0].id;
  }

  container.innerHTML = records.map((item, index) => {
    const isSelected = (item.id === selectedDocId);
    const shift = item.rank_shift;
    let rankShiftBadge = '';

    if (shift > 0) {
      rankShiftBadge = `<span class="text-[10px] px-2 py-0.5 rounded-full bg-emerald-50 dark:bg-emerald-950/70 text-emerald-600 dark:text-emerald-400 font-mono font-semibold border border-emerald-200/60 dark:border-emerald-800/60 flex items-center gap-0.5">▲ +${shift} Boost</span>`;
    } else if (shift < 0) {
      rankShiftBadge = `<span class="text-[10px] px-2 py-0.5 rounded-full bg-rose-50 dark:bg-rose-950/70 text-rose-600 dark:text-rose-400 font-mono font-semibold border border-rose-200/60 dark:border-rose-800/60 flex items-center gap-0.5">▼ ${shift} Demoted</span>`;
    } else {
      rankShiftBadge = `<span class="text-[10px] px-2 py-0.5 rounded-full bg-slate-100 dark:bg-slate-800 text-slate-500 font-mono">= Steady</span>`;
    }

    const matchedHtml = item.matched_terms && item.matched_terms.length > 0
      ? `<div class="flex flex-wrap gap-1 mt-2">${item.matched_terms.map(t => `<span class="px-2 py-0.5 rounded-md bg-indigo-50 dark:bg-indigo-950/70 text-indigo-600 dark:text-indigo-400 text-[10px] font-mono border border-indigo-200/50 dark:border-indigo-800/50">${t}</span>`).join('')}</div>`
      : '';

    return `
      <div
        id="card-${item.id}"
        onclick="selectDocumentForInspector('${item.id}')"
        class="result-card ${isSelected ? 'selected' : ''} p-4 bg-white dark:bg-slate-900 border border-slate-200/90 dark:border-slate-800 rounded-2xl shadow-sm space-y-2.5 transition-all"
      >
        <div class="flex items-start justify-between gap-3">
          <div class="flex items-start gap-3">
            <span class="w-7 h-7 rounded-xl bg-indigo-600 text-white font-mono font-bold text-xs flex items-center justify-center shadow-sm shrink-0 mt-0.5">
              ${index + 1}
            </span>
            <div>
              <h4 class="text-sm font-bold text-slate-900 dark:text-white hover:text-indigo-600 dark:hover:text-indigo-400 transition-colors line-clamp-1">
                ${item.title}
              </h4>
              <div class="flex flex-wrap items-center gap-2 mt-1 text-[11px] text-slate-500 font-mono">
                <span class="font-bold text-indigo-600 dark:text-indigo-400">${item.id}</span>
                <span>&bull;</span>
                <span class="text-slate-600 dark:text-slate-400">${item.category}</span>
                <span>&bull;</span>
                <span>${item.in_degree} citations</span>
              </div>
            </div>
          </div>
          ${rankShiftBadge}
        </div>

        <p class="text-xs text-slate-600 dark:text-slate-400 leading-relaxed pl-10">
          ${item.content_snippet}
        </p>

        ${matchedHtml ? `<div class="pl-10">${matchedHtml}</div>` : ''}

        <div class="pl-10 pt-2 border-t border-slate-100 dark:border-slate-800/80 flex items-center justify-between text-xs">
          <div class="flex items-center gap-2">
            <span class="text-[11px] font-bold text-indigo-600 dark:text-indigo-400 font-mono px-2 py-0.5 rounded-lg bg-indigo-50 dark:bg-indigo-950 border border-indigo-200/50 dark:border-indigo-800/50">
              Score: ${item.final_score.toFixed(4)}
            </span>
            <span class="text-[11px] text-slate-400 font-mono">
              (R_norm: ${item.norm_relevance.toFixed(2)} &bull; PR_norm: ${item.norm_pagerank.toFixed(2)})
            </span>
          </div>
          <span class="text-[11px] text-slate-400 hover:text-indigo-500 transition-colors font-medium flex items-center gap-1">
            <span>Inspect math</span> &rarr;
          </span>
        </div>
      </div>
    `;
  }).join('');

  // Update inspector for the selected document
  const selectedDoc = records.find(r => r.id === selectedDocId) || records[0];
  renderDocumentInspector(selectedDoc, alpha);
}

function selectDocumentForInspector(docId) {
  selectedDocId = docId;

  // Highlight selected card visually
  document.querySelectorAll('#unified-results-container .result-card').forEach(card => {
    card.classList.remove('selected');
  });
  const activeCard = document.getElementById(`card-${docId}`);
  if (activeCard) activeCard.classList.add('selected');

  if (currentSearchData && currentSearchData.combined_ranking) {
    const doc = currentSearchData.combined_ranking.find(r => r.id === docId);
    if (doc) renderDocumentInspector(doc, currentSearchData.alpha);
  }
}

function renderDocumentInspector(doc, alpha) {
  const panel = document.getElementById('unified-inspector-panel');
  if (!panel) return;

  if (!doc) {
    panel.innerHTML = `
      <div class="text-center py-10 text-slate-400 text-xs">
        No document selected.
      </div>`;
    return;
  }

  const a = (alpha !== undefined) ? alpha : 0.50;
  const contentScore = a * doc.norm_relevance;
  const authorityScore = (1.0 - a) * doc.norm_pagerank;
  const totalScore = contentScore + authorityScore;

  const contentPct = totalScore > 0 ? Math.round((contentScore / totalScore) * 100) : 50;
  const authorityPct = totalScore > 0 ? (100 - contentPct) : 50;

  panel.innerHTML = `
    <div class="space-y-4">
      
      <!-- Header -->
      <div class="border-b border-slate-100 dark:border-slate-800/80 pb-3">
        <div class="flex items-center justify-between text-xs">
          <span class="px-2 py-0.5 rounded-full bg-indigo-50 dark:bg-indigo-950 text-indigo-600 dark:text-indigo-400 font-mono font-bold text-[10px] border border-indigo-200/60 dark:border-indigo-800/60">
            ${doc.id}
          </span>
          <span class="text-slate-500 text-[11px]">${doc.category}</span>
        </div>
        <h3 class="text-sm font-bold text-slate-900 dark:text-white mt-1.5 leading-snug">
          ${doc.title}
        </h3>
      </div>

      <!-- Score Composition Visual Bar -->
      <div class="space-y-1.5">
        <div class="flex justify-between items-center text-xs">
          <span class="text-slate-600 dark:text-slate-400 font-medium">Score Composition:</span>
          <span class="font-mono text-xs font-bold text-indigo-600 dark:text-indigo-400">${doc.final_score.toFixed(4)}</span>
        </div>
        <div class="w-full h-3 rounded-full bg-slate-100 dark:bg-slate-800 overflow-hidden flex shadow-inner">
          <div style="width: ${contentPct}%" class="bg-indigo-500 h-full transition-all" title="Content Relevance: ${contentPct}%"></div>
          <div style="width: ${authorityPct}%" class="bg-violet-500 h-full transition-all" title="PageRank Authority: ${authorityPct}%"></div>
        </div>
        <div class="flex justify-between text-[10px] font-mono text-slate-500">
          <span class="text-indigo-600 dark:text-indigo-400 flex items-center gap-1"><span class="w-1.5 h-1.5 rounded-full bg-indigo-500"></span> Relevance: ${contentPct}%</span>
          <span class="text-violet-600 dark:text-violet-400 flex items-center gap-1"><span class="w-1.5 h-1.5 rounded-full bg-violet-500"></span> PageRank: ${authorityPct}%</span>
        </div>
      </div>

      <!-- Mathematical Equation Breakdown -->
      <div class="p-3 bg-slate-50 dark:bg-slate-950/70 rounded-xl border border-slate-200/70 dark:border-slate-800/80 space-y-2 text-xs">
        <div class="font-mono font-semibold text-slate-700 dark:text-slate-300 text-[11px]">
          FinalScore = &alpha;&middot;R_norm + (1-&alpha;)&middot;PR_norm
        </div>
        <div class="font-mono text-[11px] text-slate-600 dark:text-slate-400">
          = (${a.toFixed(2)} &times; ${doc.norm_relevance.toFixed(3)}) + (${(1-a).toFixed(2)} &times; ${doc.norm_pagerank.toFixed(3)})
        </div>
        <div class="font-mono text-[11px] text-indigo-600 dark:text-indigo-400 font-bold border-t border-slate-200/50 dark:border-slate-800/50 pt-1.5 flex justify-between">
          <span>= ${contentScore.toFixed(4)} + ${authorityScore.toFixed(4)}</span>
          <span>= ${doc.final_score.toFixed(4)}</span>
        </div>
      </div>

      <!-- Dimension Metrics Grid -->
      <div class="grid grid-cols-2 gap-2 text-xs font-mono">
        <div class="p-2 rounded-lg bg-slate-50 dark:bg-slate-950/50 border border-slate-200/60 dark:border-slate-800/60">
          <div class="text-[10px] text-slate-400">Raw TF-IDF Cosine</div>
          <div class="text-xs font-bold text-slate-800 dark:text-slate-200 mt-0.5">${doc.raw_relevance.toFixed(4)}</div>
        </div>
        <div class="p-2 rounded-lg bg-slate-50 dark:bg-slate-950/50 border border-slate-200/60 dark:border-slate-800/60">
          <div class="text-[10px] text-slate-400">Raw PageRank (&pi;)</div>
          <div class="text-xs font-bold text-slate-800 dark:text-slate-200 mt-0.5">${doc.raw_pagerank.toFixed(5)}</div>
        </div>
        <div class="p-2 rounded-lg bg-slate-50 dark:bg-slate-950/50 border border-slate-200/60 dark:border-slate-800/60">
          <div class="text-[10px] text-slate-400">In-Degree (Backlinks)</div>
          <div class="text-xs font-bold text-emerald-600 dark:text-emerald-400 mt-0.5">${doc.in_degree}</div>
        </div>
        <div class="p-2 rounded-lg bg-slate-50 dark:bg-slate-950/50 border border-slate-200/60 dark:border-slate-800/60">
          <div class="text-[10px] text-slate-400">Out-Degree (Links)</div>
          <div class="text-xs font-bold text-violet-600 dark:text-violet-400 mt-0.5">${doc.out_degree}</div>
        </div>
      </div>

      <!-- Rank Shift Impact -->
      <div class="p-2.5 rounded-xl bg-slate-100/70 dark:bg-slate-800/50 text-[11px] text-slate-600 dark:text-slate-400 flex items-center justify-between">
        <span>Keyword Rank: <strong class="text-slate-900 dark:text-white font-mono">#${doc.keyword_rank}</strong></span>
        <span>&rarr;</span>
        <span>Combined: <strong class="text-indigo-600 dark:text-indigo-400 font-mono">#${doc.combined_rank}</strong></span>
        <span>(${doc.rank_shift >= 0 ? '+' + doc.rank_shift : doc.rank_shift})</span>
      </div>

    </div>
  `;
}

function renderColumn(container, records, colType) {
  if (!container) return;

  if (!records || records.length === 0) {
    container.innerHTML = `
      <div class="text-center py-8 text-slate-400 text-xs">
        No documents match query.
      </div>`;
    return;
  }

  container.innerHTML = records.map((item, index) => {
    let rankBadge = '';
    let scorePill = '';
    let rankChangePill = '';

    if (colType === 'keyword') {
      rankBadge = `<span class="w-5 h-5 rounded-md bg-blue-50 dark:bg-blue-950 text-blue-600 dark:text-blue-400 font-mono font-bold text-xs flex items-center justify-center">${index + 1}</span>`;
      scorePill = `<span class="text-blue-600 dark:text-blue-400 font-mono text-[10px]">TF-IDF: ${item.raw_relevance.toFixed(3)}</span>`;
    } else if (colType === 'pagerank') {
      rankBadge = `<span class="w-5 h-5 rounded-md bg-purple-50 dark:bg-purple-950 text-purple-600 dark:text-purple-400 font-mono font-bold text-xs flex items-center justify-center">${index + 1}</span>`;
      scorePill = `<span class="text-purple-600 dark:text-purple-400 font-mono text-[10px]">PR: ${item.raw_pagerank.toFixed(4)}</span>`;
    } else {
      rankBadge = `<span class="w-5 h-5 rounded-md bg-indigo-600 text-white font-mono font-bold text-xs flex items-center justify-center shadow-sm">${index + 1}</span>`;
      scorePill = `<span class="text-indigo-600 dark:text-indigo-400 font-mono font-bold text-[10px]">Score: ${item.final_score.toFixed(3)}</span>`;

      const shift = item.rank_shift;
      if (shift > 0) {
        rankChangePill = `<span class="text-[10px] px-1.5 py-0.2 rounded bg-emerald-50 dark:bg-emerald-950 text-emerald-600 dark:text-emerald-400 font-mono font-semibold">▲ +${shift}</span>`;
      } else if (shift < 0) {
        rankChangePill = `<span class="text-[10px] px-1.5 py-0.2 rounded bg-rose-50 dark:bg-rose-950 text-rose-600 dark:text-rose-400 font-mono font-semibold">▼ ${shift}</span>`;
      } else {
        rankChangePill = `<span class="text-[10px] px-1.5 py-0.2 rounded bg-slate-100 dark:bg-slate-800 text-slate-500 font-mono">=</span>`;
      }
    }

    return `
      <div class="result-card p-3 bg-slate-50/80 dark:bg-slate-950 border border-slate-200/80 dark:border-slate-800/80 rounded-xl space-y-1.5">
        <div class="flex items-start justify-between gap-2">
          <div class="flex items-start gap-2">
            ${rankBadge}
            <div>
              <div class="text-xs font-bold text-slate-900 dark:text-slate-100 line-clamp-1">${item.title}</div>
              <div class="flex items-center gap-2 mt-0.5 text-[10px] text-slate-500 font-mono">
                <span>${item.id}</span>
                <span>&bull;</span>
                <span>${item.category}</span>
                <span>&bull;</span>
                <span>In: ${item.in_degree}</span>
              </div>
            </div>
          </div>
          ${rankChangePill}
        </div>

        <p class="text-[11px] text-slate-600 dark:text-slate-400 leading-snug line-clamp-2">${item.content_snippet}</p>

        <div class="pt-1.5 border-t border-slate-200/70 dark:border-slate-800/70 flex items-center justify-between text-[10px]">
          ${scorePill}
          <div class="text-slate-400 font-mono">
            R_n: ${item.norm_relevance.toFixed(2)} | PR_n: ${item.norm_pagerank.toFixed(2)}
          </div>
        </div>
      </div>
    `;
  }).join('');
}

// --------------------------------------------------------------------------
// 2. WEB GRAPH NETWORK EXPLORER
// --------------------------------------------------------------------------

function initNetworkGraph() {
  const container = document.getElementById('network-canvas');
  if (!container) return;

  const isDark = (currentTheme === 'dark');

  const options = {
    nodes: {
      shape: 'dot',
      font: {
        color: isDark ? '#F8FAFC' : '#0F172A',
        face: 'Plus Jakarta Sans',
        size: 12,
        bold: { color: isDark ? '#FFFFFF' : '#000000' }
      },
      borderWidth: 2,
      shadow: false
    },
    edges: {
      arrows: { to: { enabled: true, scaleFactor: 0.55 } },
      smooth: { type: 'continuous' },
      color: {
        color: isDark ? '#64748B' : '#94A3B8',
        highlight: '#4F46E5'
      },
      width: 1.2
    },
    physics: {
      enabled: true,
      solver: 'forceAtlas2Based',
      forceAtlas2Based: {
        gravitationalConstant: -40,
        centralGravity: 0.009,
        springLength: 85,
        springConstant: 0.12,
        damping: 0.88
      },
      stabilization: { iterations: 100 }
    },
    interaction: {
      hover: true,
      tooltipDelay: 120
    }
  };

  networkData = {
    nodes: new vis.DataSet([]),
    edges: new vis.DataSet([])
  };

  networkInstance = new vis.Network(container, networkData, options);

  networkInstance.on('click', params => {
    if (params.nodes.length > 0) {
      inspectNode(params.nodes[0]);
    }
  });

  loadGraphData();
}

async function loadGraphData() {
  const damping = parseFloat(document.getElementById('damping-slider').value) || 0.85;
  try {
    const res = await fetch(`/api/graph?damping=${damping}`);
    const data = await res.json();
    graphCache = data;

    networkData.nodes.clear();
    networkData.edges.clear();
    networkData.nodes.add(data.nodes);
    networkData.edges.add(data.edges);

    populateNodeSelects();
  } catch (err) {
    console.error('Failed to load graph data:', err);
  }
}

function inspectNode(nodeId) {
  if (!graphCache) return;
  const node = graphCache.nodes.find(n => n.id === nodeId);
  if (!node) return;

  document.getElementById('inspect-node-id').innerText = node.id;
  
  const inLinks = graphCache.edges.filter(e => e.to === nodeId).map(e => e.from);
  const outLinks = graphCache.edges.filter(e => e.from === nodeId).map(e => e.to);

  const body = document.getElementById('inspect-node-body');
  body.innerHTML = `
    <div class="space-y-2">
      <div class="font-bold text-slate-900 dark:text-white text-xs">${node.page_title}</div>
      <div class="text-[11px] text-slate-500">${node.content_snippet}</div>
      
      <div class="grid grid-cols-2 gap-2 pt-2 border-t border-slate-200 dark:border-slate-800 font-mono text-[11px]">
        <div><span class="text-slate-400">PageRank:</span> <span class="text-indigo-600 dark:text-indigo-400 font-bold">${node.pagerank.toFixed(5)}</span></div>
        <div><span class="text-slate-400">In-Degree:</span> <span class="font-bold">${node.in_degree}</span></div>
        <div><span class="text-slate-400">Out-Degree:</span> <span class="font-bold">${node.out_degree}</span></div>
        <div><span class="text-slate-400">Category:</span> <span>${node.category}</span></div>
      </div>

      <div class="pt-2 border-t border-slate-200 dark:border-slate-800">
        <span class="text-[11px] text-slate-400 block mb-1">In-links (${inLinks.length}):</span>
        <div class="flex flex-wrap gap-1">${inLinks.length ? inLinks.map(l => `<span class="px-1.5 py-0.2 rounded bg-slate-100 dark:bg-slate-800 text-slate-700 dark:text-slate-300 font-mono text-[10px]">${l}</span>`).join('') : '<span class="text-slate-400">None</span>'}</div>
      </div>

      <div class="pt-1.5">
        <span class="text-[11px] text-slate-400 block mb-1">Out-links (${outLinks.length}):</span>
        <div class="flex flex-wrap gap-1">${outLinks.length ? outLinks.map(l => `<span class="px-1.5 py-0.2 rounded bg-slate-100 dark:bg-slate-800 text-slate-700 dark:text-slate-300 font-mono text-[10px]">${l}</span>`).join('') : '<span class="text-rose-500 font-mono">Dangling Node</span>'}</div>
      </div>
    </div>
  `;
}

function fitGraphView() {
  if (networkInstance) networkInstance.fit({ animation: { duration: 500, easingFunction: 'easeInOutQuad' } });
}

let physicsEnabled = true;
function toggleGraphPhysics() {
  physicsEnabled = !physicsEnabled;
  if (networkInstance) {
    networkInstance.setOptions({ physics: { enabled: physicsEnabled } });
    document.getElementById('physics-toggle-btn').innerText = physicsEnabled ? 'Freeze Physics' : 'Unfreeze Physics';
  }
}

async function populateNodeSelects() {
  try {
    const res = await fetch('/api/corpus');
    const pages = await res.json();
    const sourceSelect = document.getElementById('edge-source-select');
    const targetSelect = document.getElementById('edge-target-select');

    if (!sourceSelect || !targetSelect) return;

    const optionsHtml = pages.map(p => `<option value="${p.id}">${p.id} - ${p.title.slice(0, 26)}...</option>`).join('');
    sourceSelect.innerHTML = optionsHtml;
    targetSelect.innerHTML = optionsHtml;
    if (pages.length > 1) targetSelect.selectedIndex = 1;
  } catch (err) {
    console.error('Failed to populate node selects:', err);
  }
}

async function addLinkDynamic() {
  const source = document.getElementById('edge-source-select').value;
  const target = document.getElementById('edge-target-select').value;
  if (source === target) return alert("Source and target must be distinct nodes.");

  const res = await fetch('/api/graph/add_link', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ source, target })
  });
  const data = await res.json();
  if (data.success) {
    await loadGraphData();
    triggerSearch();
  }
}

async function removeLinkDynamic() {
  const source = document.getElementById('edge-source-select').value;
  const target = document.getElementById('edge-target-select').value;

  const res = await fetch('/api/graph/remove_link', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ source, target })
  });
  const data = await res.json();
  if (data.success) {
    await loadGraphData();
    triggerSearch();
  }
}

async function resetGraphToDefault() {
  if (!confirm("Reset web graph back to baseline corpus?")) return;
  const res = await fetch('/api/graph/reset', { method: 'POST' });
  const data = await res.json();
  if (data.success) {
    const spamRes = document.getElementById('spam-experiment-results');
    if (spamRes) spamRes.classList.add('hidden');
    const trapRes = document.getElementById('trap-experiment-results');
    if (trapRes) trapRes.classList.add('hidden');
    await loadGraphData();
    triggerSearch();
  }
}

// --------------------------------------------------------------------------
// 3. MARKOV RANDOM SURFER LAB
// --------------------------------------------------------------------------

async function runRandomWalkSimulation() {
  const numSteps = parseInt(document.getElementById('surfer-steps-select').value);
  const damping = parseFloat(document.getElementById('damping-slider').value);

  try {
    const res = await fetch('/api/random_walk', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ num_steps: numSteps, damping: damping })
    });
    const simData = await res.json();
    renderSurferResults(simData);
  } catch (err) {
    console.error('Random walk simulation failed:', err);
  }
}

function renderSurferResults(data) {
  document.getElementById('walk-start-node').innerText = data.start_node;
  document.getElementById('walk-total-steps').innerText = data.num_steps.toLocaleString();
  document.getElementById('walk-end-node').innerText = data.end_node;
  document.getElementById('surfer-l1-badge').innerText = `L1 Error: ${data.final_l1_error.toFixed(4)}`;

  const trajectoryList = document.getElementById('walk-trajectory-list');
  const sample = data.trajectory_sample || [];
  trajectoryList.innerHTML = sample.map((node, i) => {
    return `<div class="flex items-center gap-1.5"><span class="text-slate-400 text-[10px]">#${i}</span> <span class="text-pink-600 dark:text-pink-400 font-bold">${node}</span></div>`;
  }).join('');

  const labels = Object.keys(data.empirical_distribution);
  const empiricalProbs = labels.map(k => data.empirical_distribution[k]);
  const theoreticalProbs = labels.map(k => data.theoretical_distribution ? data.theoretical_distribution[k] : 0);

  const isDark = (currentTheme === 'dark');
  const textColor = isDark ? '#94A3B8' : '#475569';
  const gridColor = isDark ? 'rgba(51, 65, 85, 0.3)' : 'rgba(226, 232, 240, 0.8)';
  const legendColor = isDark ? '#E2E8F0' : '#1E293B';

  const ctx = document.getElementById('surferComparisonChart').getContext('2d');
  if (surferChartInstance) surferChartInstance.destroy();

  surferChartInstance = new Chart(ctx, {
    type: 'bar',
    data: {
      labels: labels,
      datasets: [
        {
          label: 'Empirical Visit Frequency π̂',
          data: empiricalProbs,
          backgroundColor: 'rgba(236, 72, 153, 0.8)',
          borderRadius: 3
        },
        {
          label: 'Theoretical PageRank π',
          data: theoreticalProbs,
          backgroundColor: 'rgba(99, 102, 241, 0.5)',
          borderRadius: 3
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { labels: { color: legendColor, font: { size: 11 } } }
      },
      scales: {
        x: { ticks: { color: textColor, font: { size: 10 } }, grid: { color: gridColor } },
        y: { ticks: { color: textColor, font: { size: 10 } }, grid: { color: gridColor } }
      }
    }
  });
}

// --------------------------------------------------------------------------
// 4. EXPERIMENTS LAB
// --------------------------------------------------------------------------

async function runSpamExperiment() {
  try {
    const res = await fetch('/api/experiments/spam?target_id=page_16&num_bots=5');
    const data = await res.json();

    const container = document.getElementById('spam-experiment-results');
    container.classList.remove('hidden');
    container.innerHTML = `
      <div class="font-bold text-rose-600 dark:text-rose-400">Sybil Attack Injected!</div>
      <div class="grid grid-cols-2 gap-1 text-slate-700 dark:text-slate-300 font-mono text-[11px] pt-1">
        <div>Baseline PR: ${data.baseline_pr.toFixed(5)}</div>
        <div>New PR: <span class="font-bold text-rose-600 dark:text-rose-400">${data.spam_pr.toFixed(5)}</span></div>
        <div>Gain: <span class="text-emerald-600 dark:text-emerald-400 font-bold">+${data.pr_percentage_gain}%</span></div>
        <div>Rank: <span class="text-amber-600 dark:text-amber-400 font-bold">#${data.baseline_combined_rank} &rarr; #${data.spam_combined_rank}</span></div>
      </div>
    `;

    await loadGraphData();
    triggerSearch();
  } catch (err) {
    console.error('Spam experiment failed:', err);
  }
}

async function runSpiderTrapExperiment() {
  try {
    const res = await fetch('/api/experiments/trap');
    const data = await res.json();

    const container = document.getElementById('trap-experiment-results');
    container.classList.remove('hidden');
    container.innerHTML = `
      <div class="font-bold text-amber-600 dark:text-amber-400">Spider Trap Simulation Done!</div>
      <div class="space-y-1 text-slate-700 dark:text-slate-300 font-mono text-[11px] pt-1">
        <div>Trap Mass with Teleportation (d=0.85): <span class="text-emerald-600 dark:text-emerald-400 font-bold">${(data.trap_mass_with_damping_085 * 100).toFixed(1)}%</span></div>
        <div>Trap Mass without Escape (d=0.99): <span class="text-rose-600 dark:text-rose-400 font-bold">${(data.trap_mass_with_damping_099 * 100).toFixed(1)}%</span></div>
        <div class="text-[10px] text-slate-500 font-sans italic pt-0.5">
          ${data.theoretical_insight}
        </div>
      </div>
    `;

    await loadGraphData();
    triggerSearch();
  } catch (err) {
    console.error('Spider trap experiment failed:', err);
  }
}

async function loadDampingExperiment() {
  try {
    const res = await fetch('/api/experiments/damping');
    const data = await res.json();

    const dValues = data.map(item => item.damping_factor);
    const entropies = data.map(item => item.entropy);
    const iterations = data.map(item => item.iterations);

    const isDark = (currentTheme === 'dark');
    const textColor = isDark ? '#94A3B8' : '#475569';
    const gridColor = isDark ? 'rgba(51, 65, 85, 0.3)' : 'rgba(226, 232, 240, 0.8)';
    const legendColor = isDark ? '#E2E8F0' : '#1E293B';

    const ctx = document.getElementById('dampingSensitivityChart').getContext('2d');
    if (dampingChartInstance) dampingChartInstance.destroy();

    dampingChartInstance = new Chart(ctx, {
      type: 'line',
      data: {
        labels: dValues.map(d => `d=${d}`),
        datasets: [
          {
            label: 'Entropy (bits)',
            data: entropies,
            borderColor: '#8B5CF6',
            backgroundColor: 'rgba(139, 92, 246, 0.1)',
            fill: true,
            tension: 0.3,
            yAxisID: 'y'
          },
          {
            label: 'Iterations to Converge',
            data: iterations,
            borderColor: '#F59E0B',
            borderDash: [4, 4],
            fill: false,
            tension: 0.2,
            yAxisID: 'y1'
          }
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { labels: { color: legendColor, font: { size: 11 } } }
        },
        scales: {
          x: { ticks: { color: textColor, font: { size: 10 } }, grid: { color: gridColor } },
          y: {
            type: 'linear',
            position: 'left',
            title: { display: true, text: 'Entropy', color: textColor, font: { size: 10 } },
            ticks: { color: textColor, font: { size: 10 } },
            grid: { color: gridColor }
          },
          y1: {
            type: 'linear',
            position: 'right',
            title: { display: true, text: 'Iterations', color: textColor, font: { size: 10 } },
            ticks: { color: textColor, font: { size: 10 } },
            grid: { drawOnChartArea: false }
          }
        }
      }
    });
  } catch (err) {
    console.error('Failed to load damping experiment:', err);
  }
}
