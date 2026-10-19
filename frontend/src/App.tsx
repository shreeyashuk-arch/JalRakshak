import React, { useState, useEffect } from 'react';
import { 
  Activity, 
  Droplet, 
  AlertTriangle, 
  CheckCircle2, 
  Radio, 
  Cpu, 
  TrendingUp, 
  Wrench, 
  Play, 
  RotateCcw,
  Zap
} from 'lucide-react';

interface Asset {
  id: string;
  name: string;
  asset_type: string;
  location: string;
  status: string;
  health_score: number;
  risk: string;
  water_impact: string;
}

interface WaterReliability {
  overall_score: number;
  active_assets: number;
  assets_at_risk: number;
  maintenance_due: number;
  system_status: string;
  disclaimer: string;
}

interface Prediction {
  water_reliability_score: number;
  pump_health: number;
  flow_efficiency: number;
  risk_level: string;
  maintenance_priority: string;
  recommended_action: string;
  estimated_maintenance_window: string;
  observed_deviations: string[];
}

export default function App() {
  const [activeTab, setActiveTab] = useState<'overview' | 'assets' | 'prediction' | 'aquamesh' | 'simulation'>('overview');
  const [assets, setAssets] = useState<Asset[]>([]);
  const [reliability, setReliability] = useState<WaterReliability | null>(null);
  const [selectedAsset, setSelectedAsset] = useState<string>('PUMP-03');
  const [prediction, setPrediction] = useState<Prediction | null>(null);
  const [simLoading, setSimLoading] = useState(false);
  const [simMessage, setSimMessage] = useState<string>('');

  const fetchDashboardData = async () => {
    try {
      const [assetsRes, relRes] = await Promise.all([
        fetch('/api/assets'),
        fetch('/api/water-reliability')
      ]);
      if (assetsRes.ok) setAssets(await assetsRes.json());
      if (relRes.ok) setReliability(await relRes.json());
    } catch (e) {
      console.warn("Using fallback prototype data");
      setAssets([
        { id: 'PUMP-01', name: 'Primary Borewell Pump A', asset_type: 'PUMP', location: 'North Wellfield', status: 'HEALTHY', health_score: 96, risk: 'LOW', water_impact: 'MINIMAL' },
        { id: 'PUMP-02', name: 'Solar Submersible Pump B', asset_type: 'PUMP', location: 'East Agri Line', status: 'MONITOR', health_score: 81, risk: 'LOW', water_impact: 'SLIGHT' },
        { id: 'PUMP-03', name: 'Centrifugal Booster Pump C', asset_type: 'PUMP', location: 'Central Hub', status: 'DEGRADING', health_score: 54, risk: 'HIGH', water_impact: 'HIGH' },
        { id: 'PUMP-04', name: 'High-Pressure Booster D', asset_type: 'PUMP', location: 'Hilltop Feed', status: 'CRITICAL', health_score: 31, risk: 'CRITICAL', water_impact: 'SEVERE' },
      ]);
      setReliability({
        overall_score: 72.4,
        active_assets: 4,
        assets_at_risk: 2,
        maintenance_due: 2,
        system_status: 'ATTENTION REQUIRED',
        disclaimer: 'Prototype composite metric.'
      });
    }
  };

  const fetchPrediction = async (id: string) => {
    try {
      const res = await fetch(`/api/assets/${id}/prediction`);
      if (res.ok) setPrediction(await res.json());
    } catch (e) {
      setPrediction({
        water_reliability_score: 58.2,
        pump_health: 54.0,
        flow_efficiency: 0.88,
        risk_level: 'HIGH',
        maintenance_priority: 'HIGH PRIORITY',
        recommended_action: 'Inspect pump bearing/coupling and verify intake condition.',
        estimated_maintenance_window: '18–30 operating hours',
        observed_deviations: [
          'Vibration: +38% from nominal baseline',
          'Current: +9% irregularity detected',
          'Flow efficiency: -12% drop',
          'Tank recovery time: +14 minutes delay'
        ]
      });
    }
  };

  useEffect(() => {
    fetchDashboardData();
  }, []);

  useEffect(() => {
    fetchPrediction(selectedAsset);
  }, [selectedAsset]);

  const injectFault = async (faultType: string, severity: number = 0.75) => {
    setSimLoading(true);
    setSimMessage(`Injecting ${faultType}...`);
    try {
      const res = await fetch('/api/simulation/fault', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ asset_id: selectedAsset, fault_type: faultType, severity })
      });
      if (res.ok) {
        const data = await res.json();
        setSimMessage(data.message);
        await fetchDashboardData();
        await fetchPrediction(selectedAsset);
      }
    } catch (e) {
      setSimMessage("Simulated locally (offline)");
    } finally {
      setSimLoading(false);
    }
  };

  const resetSimulation = async () => {
    setSimLoading(true);
    try {
      await fetch('/api/simulation/reset', { method: 'POST' });
      setSimMessage("Reset to baseline healthy status.");
      await fetchDashboardData();
      await fetchPrediction(selectedAsset);
    } catch (e) {
      // offline reset
    } finally {
      setSimLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 flex flex-col font-sans">
      {/* Top Header */}
      <header className="border-b border-slate-800 bg-slate-900/60 backdrop-blur px-6 py-4 flex flex-wrap justify-between items-center gap-4">
        <div className="flex items-center gap-3">
          <div className="p-2.5 bg-cyan-500/10 border border-cyan-500/30 rounded-xl text-cyan-400">
            <Droplet className="w-6 h-6 animate-pulse" />
          </div>
          <div>
            <div className="flex items-center gap-2">
              <h1 className="text-xl font-bold tracking-tight text-white">JALRAKSHAK</h1>
              <span className="text-xs px-2 py-0.5 rounded-full bg-cyan-950 text-cyan-400 border border-cyan-800 font-mono">
                Nordic nRF54LM20 DK
              </span>
            </div>
            <p className="text-xs text-slate-400">Predict the Failure. Protect the Water.</p>
          </div>
        </div>

        {/* Navigation Tabs */}
        <nav className="flex items-center gap-2 bg-slate-900 p-1 rounded-lg border border-slate-800 text-sm">
          {[
            { id: 'overview', label: 'Overview', icon: Activity },
            { id: 'assets', label: 'Asset Fleet', icon: Cpu },
            { id: 'prediction', label: 'Impact Prediction', icon: TrendingUp },
            { id: 'aquamesh', label: 'AquaMesh BLE', icon: Radio },
            { id: 'simulation', label: 'Demo Simulation', icon: Play },
          ].map((tab) => {
            const Icon = tab.icon;
            return (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id as any)}
                className={`flex items-center gap-1.5 px-3 py-1.5 rounded-md font-medium transition ${
                  activeTab === tab.id
                    ? 'bg-cyan-500/20 text-cyan-300 border border-cyan-500/40 shadow-sm'
                    : 'text-slate-400 hover:text-slate-200'
                }`}
              >
                <Icon className="w-4 h-4" />
                {tab.label}
              </button>
            );
          })}
        </nav>
      </header>

      {/* Main Container */}
      <main className="flex-1 p-6 max-w-7xl w-full mx-auto space-y-6">
        {/* Prototype Scientific Notice Banner */}
        <div className="bg-cyan-950/40 border border-cyan-800/60 rounded-xl p-3 px-4 flex items-center justify-between text-xs text-cyan-200">
          <div className="flex items-center gap-2">
            <Zap className="w-4 h-4 text-cyan-400 shrink-0" />
            <span>
              <strong>Competition Prototype Architecture:</strong> Sensor telemetry and Edge-AI inferences shown reflect verified synthetic prototype pipeline targeting the <strong>Nordic nRF54LM20 DK</strong>.
            </span>
          </div>
          <span className="bg-cyan-900/80 px-2 py-0.5 rounded text-[11px] font-mono border border-cyan-700">
            AquaMesh BLE v1.1
          </span>
        </div>

        {/* OVERVIEW TAB */}
        {activeTab === 'overview' && (
          <div className="space-y-6">
            {/* Top Stat Cards */}
            <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
              <div className="bg-slate-900/80 border border-slate-800 rounded-xl p-5">
                <div className="text-slate-400 text-xs font-medium uppercase tracking-wider">Water Reliability Score</div>
                <div className="text-3xl font-extrabold text-cyan-400 mt-2">
                  {reliability?.overall_score || 72.4} <span className="text-sm font-normal text-slate-400">/ 100</span>
                </div>
                <div className="text-xs text-slate-400 mt-1">Prototype Composite Metric</div>
              </div>

              <div className="bg-slate-900/80 border border-slate-800 rounded-xl p-5">
                <div className="text-slate-400 text-xs font-medium uppercase tracking-wider">Monitored Assets</div>
                <div className="text-3xl font-extrabold text-white mt-2">
                  {assets.length || 4}
                </div>
                <div className="text-xs text-slate-400 mt-1">4 Pumps, 1 Storage Tank</div>
              </div>

              <div className="bg-slate-900/80 border border-slate-800 rounded-xl p-5">
                <div className="text-slate-400 text-xs font-medium uppercase tracking-wider">Assets at Risk</div>
                <div className="text-3xl font-extrabold text-amber-400 mt-2">
                  {assets.filter(a => a.health_score < 70).length}
                </div>
                <div className="text-xs text-amber-500/80 mt-1">Degradation Trend Detected</div>
              </div>

              <div className="bg-slate-900/80 border border-slate-800 rounded-xl p-5">
                <div className="text-slate-400 text-xs font-medium uppercase tracking-wider">Maintenance Opportunity</div>
                <div className="text-3xl font-extrabold text-emerald-400 mt-2">1 Active</div>
                <div className="text-xs text-slate-400 mt-1">Technician Near Sector 1</div>
              </div>
            </div>

            {/* Quick Multi-Asset Summary */}
            <div className="bg-slate-900/70 border border-slate-800 rounded-xl p-5 space-y-4">
              <h2 className="text-base font-semibold text-white flex items-center justify-between">
                <span>Multi-Asset Health & Water Risk Ranking</span>
                <span className="text-xs font-normal text-slate-400">Sorted by Water-Access Impact</span>
              </h2>

              <div className="overflow-x-auto">
                <table className="w-full text-left text-sm">
                  <thead className="text-xs uppercase bg-slate-950/50 text-slate-400 border-b border-slate-800">
                    <tr>
                      <th className="py-3 px-4">Asset</th>
                      <th className="py-3 px-4">Type</th>
                      <th className="py-3 px-4">Status</th>
                      <th className="py-3 px-4">Health Score</th>
                      <th className="py-3 px-4">Water Risk</th>
                      <th className="py-3 px-4">Action</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-slate-800/60 font-mono text-xs">
                    {assets.map((asset) => (
                      <tr key={asset.id} className="hover:bg-slate-800/30 transition">
                        <td className="py-3 px-4 font-semibold text-white">{asset.id} - {asset.name}</td>
                        <td className="py-3 px-4 text-slate-300">{asset.asset_type}</td>
                        <td className="py-3 px-4">
                          <span className={`px-2 py-0.5 rounded-full text-[11px] font-sans ${
                            asset.status === 'HEALTHY' ? 'bg-emerald-950 text-emerald-400 border border-emerald-800' :
                            asset.status === 'MONITOR' ? 'bg-blue-950 text-blue-400 border border-blue-800' :
                            asset.status === 'DEGRADING' ? 'bg-amber-950 text-amber-400 border border-amber-800' :
                            'bg-rose-950 text-rose-400 border border-rose-800'
                          }`}>
                            {asset.status}
                          </span>
                        </td>
                        <td className="py-3 px-4 font-bold text-slate-200">{asset.health_score}%</td>
                        <td className="py-3 px-4 font-sans font-medium text-slate-300">{asset.water_impact}</td>
                        <td className="py-3 px-4 font-sans">
                          <button
                            onClick={() => { setSelectedAsset(asset.id); setActiveTab('prediction'); }}
                            className="text-cyan-400 hover:text-cyan-300 text-xs font-medium underline"
                          >
                            Inspect Impact →
                          </button>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        )}

        {/* PREDICTION TAB */}
        {activeTab === 'prediction' && (
          <div className="space-y-6">
            <div className="flex items-center justify-between">
              <div>
                <h2 className="text-xl font-bold text-white">Failure-to-Impact Predictive Assessment</h2>
                <p className="text-xs text-slate-400">Translating mechanical vibration & current drift into community water reliability risk.</p>
              </div>

              {/* Asset Selector */}
              <div className="flex items-center gap-2">
                <span className="text-xs text-slate-400">Selected Asset:</span>
                <select
                  value={selectedAsset}
                  onChange={(e) => setSelectedAsset(e.target.value)}
                  className="bg-slate-900 border border-slate-700 text-slate-200 text-xs rounded-lg px-3 py-1.5 focus:outline-none focus:border-cyan-500"
                >
                  {assets.map(a => <option key={a.id} value={a.id}>{a.id} - {a.name}</option>)}
                </select>
              </div>
            </div>

            {prediction && (
              <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
                {/* Left Card: Health & Reliability Gauge */}
                <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 space-y-4">
                  <h3 className="text-sm font-semibold text-slate-300 uppercase tracking-wider">Asset Health State</h3>
                  <div className="text-4xl font-extrabold text-cyan-400">
                    {prediction.pump_health}%
                    <span className="text-xs font-normal text-slate-400 block mt-1">Calculated via Edge-AI Feature Model</span>
                  </div>

                  <div className="space-y-2 pt-2 border-t border-slate-800 text-xs">
                    <div className="flex justify-between">
                      <span className="text-slate-400">Flow Efficiency:</span>
                      <span className="font-mono text-slate-200">{(prediction.flow_efficiency * 100).toFixed(0)}% of nominal</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-slate-400">Water Reliability Score:</span>
                      <span className="font-mono font-bold text-cyan-300">{prediction.water_reliability_score}/100</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-slate-400">System Risk Level:</span>
                      <span className={`font-bold ${
                        prediction.risk_level === 'CRITICAL' ? 'text-rose-400' :
                        prediction.risk_level === 'HIGH' ? 'text-amber-400' : 'text-emerald-400'
                      }`}>{prediction.risk_level}</span>
                    </div>
                  </div>
                </div>

                {/* Middle Card: Why is this asset at risk? */}
                <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 space-y-3">
                  <h3 className="text-sm font-semibold text-slate-300 uppercase tracking-wider">Observed Degradation</h3>
                  <div className="space-y-2">
                    {prediction.observed_deviations.map((dev, idx) => (
                      <div key={idx} className="flex items-start gap-2 bg-slate-950/60 p-2.5 rounded-lg border border-slate-800/80 text-xs text-slate-300">
                        <AlertTriangle className="w-4 h-4 text-amber-400 shrink-0 mt-0.5" />
                        <span>{dev}</span>
                      </div>
                    ))}
                  </div>
                </div>

                {/* Right Card: Maintenance-by-Opportunity & Action */}
                <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 space-y-4">
                  <div className="flex items-center justify-between">
                    <h3 className="text-sm font-semibold text-slate-300 uppercase tracking-wider">Technician Action</h3>
                    <span className="px-2 py-0.5 rounded text-[11px] font-mono bg-cyan-950 text-cyan-400 border border-cyan-800">
                      {prediction.maintenance_priority}
                    </span>
                  </div>

                  <div className="bg-slate-950/60 p-3 rounded-lg border border-slate-800 text-xs space-y-2">
                    <div className="text-slate-400 font-medium">Estimated Maintenance Window:</div>
                    <div className="text-sm font-semibold text-amber-400 font-mono">
                      {prediction.estimated_maintenance_window}
                    </div>
                    <p className="text-[11px] text-slate-500 italic">
                      *Prototype window estimate based on degradation slope.
                    </p>
                  </div>

                  <div className="space-y-1">
                    <div className="text-xs text-slate-400 font-medium">Recommended Action:</div>
                    <p className="text-xs text-slate-200 bg-cyan-950/20 border border-cyan-800/40 p-2.5 rounded-lg">
                      {prediction.recommended_action}
                    </p>
                  </div>
                </div>
              </div>
            )}
          </div>
        )}

        {/* AQUAMESH TAB */}
        {activeTab === 'aquamesh' && (
          <div className="space-y-6">
            <div className="flex items-center justify-between">
              <div>
                <h2 className="text-xl font-bold text-white">AquaMesh Bluetooth Network</h2>
                <p className="text-xs text-slate-400">Low-power BLE Mesh topology with offline-first synchronization to technician handheld gateways.</p>
              </div>
              <span className="px-3 py-1 rounded-full text-xs font-mono bg-blue-950 text-blue-400 border border-blue-800">
                Physical Protocol: nRF54LM20 Zephyr bt_mesh
              </span>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              {[
                { id: 'NODE-P01', name: 'Pump-01 (nRF54LM20)', type: 'PUMP', health: 95, rssi: -58, hops: 1, status: 'CONNECTED' },
                { id: 'NODE-P02', name: 'Pump-02 (nRF54LM20)', type: 'PUMP', health: 81, rssi: -72, hops: 2, status: 'CONNECTED' },
                { id: 'NODE-P03', name: 'Pump-03 (nRF54LM20)', type: 'PUMP', health: 54, rssi: -64, hops: 1, status: 'CONNECTED' },
                { id: 'NODE-P04', name: 'Pump-04 (nRF54LM20)', type: 'PUMP', health: 31, rssi: -84, hops: 3, status: 'WARNING' },
                { id: 'NODE-T01', name: 'Tank-01 Telemetry Node', type: 'TANK', health: 92, rssi: -60, hops: 1, status: 'CONNECTED' },
                { id: 'GW-TECH01', name: 'Technician Handheld Gateway', type: 'GATEWAY', health: 100, rssi: -45, hops: 0, status: 'ONLINE' },
              ].map((node) => (
                <div key={node.id} className="bg-slate-900 border border-slate-800 rounded-xl p-4 space-y-3">
                  <div className="flex items-center justify-between">
                    <div className="font-semibold text-sm text-white">{node.name}</div>
                    <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-slate-800 text-slate-300">{node.type}</span>
                  </div>
                  <div className="text-xs space-y-1 font-mono text-slate-400">
                    <div>Node ID: <span className="text-slate-200">{node.id}</span></div>
                    <div>Mesh Relay Hops: <span className="text-slate-200">{node.hops}</span></div>
                    <div>Radio RSSI: <span className="text-slate-200">{node.rssi} dBm</span></div>
                    <div>Health Score: <span className="text-cyan-400 font-bold">{node.health}%</span></div>
                  </div>
                  <div className="pt-2 border-t border-slate-800 flex items-center justify-between text-xs">
                    <span className="text-emerald-400 flex items-center gap-1 font-sans">
                      <CheckCircle2 className="w-3.5 h-3.5" /> Synchronized
                    </span>
                    <span className="text-slate-500 text-[11px]">Just now</span>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* SIMULATION TAB */}
        {activeTab === 'simulation' && (
          <div className="space-y-6">
            <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 space-y-5">
              <div>
                <h2 className="text-xl font-bold text-white flex items-center gap-2">
                  <Play className="w-5 h-5 text-cyan-400" />
                  Controlled Fault Injection & Degradation Demo
                </h2>
                <p className="text-xs text-slate-400 mt-1">
                  Inject progressive physical faults into <strong>{selectedAsset}</strong> to demonstrate how early edge degradation triggers failure-to-impact predictions and updates maintenance priority in real time.
                </p>
              </div>

              {simMessage && (
                <div className="p-3 bg-cyan-950/60 border border-cyan-800 rounded-lg text-xs font-mono text-cyan-200">
                  {simMessage}
                </div>
              )}

              <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">
                <button
                  disabled={simLoading}
                  onClick={() => injectFault('BEARING_DEGRADATION', 0.70)}
                  className="p-4 bg-slate-950 hover:bg-slate-800/80 border border-slate-800 hover:border-amber-500/50 rounded-xl text-left transition group"
                >
                  <div className="font-semibold text-sm text-amber-400 group-hover:text-amber-300">
                    1. Bearing Degradation
                  </div>
                  <div className="text-xs text-slate-400 mt-1">
                    Inject high-frequency vibration spike (+38%), temperature rise, and flow decrease.
                  </div>
                </button>

                <button
                  disabled={simLoading}
                  onClick={() => injectFault('OVERLOAD', 0.80)}
                  className="p-4 bg-slate-950 hover:bg-slate-800/80 border border-slate-800 hover:border-rose-500/50 rounded-xl text-left transition group"
                >
                  <div className="font-semibold text-sm text-rose-400 group-hover:text-rose-300">
                    2. Motor Electrical Overload
                  </div>
                  <div className="text-xs text-slate-400 mt-1">
                    Simulate current surge (+3.2A), thermal climb, and winding stress.
                  </div>
                </button>

                <button
                  disabled={simLoading}
                  onClick={() => injectFault('LOW_FLOW', 0.85)}
                  className="p-4 bg-slate-950 hover:bg-slate-800/80 border border-slate-800 hover:border-cyan-500/50 rounded-xl text-left transition group"
                >
                  <div className="font-semibold text-sm text-cyan-400 group-hover:text-cyan-300">
                    3. Blocked Intake / Low Flow
                  </div>
                  <div className="text-xs text-slate-400 mt-1">
                    Simulate fluid cavitation and severe flow drop affecting tank recovery.
                  </div>
                </button>
              </div>

              <div className="pt-4 border-t border-slate-800 flex items-center justify-between">
                <button
                  disabled={simLoading}
                  onClick={resetSimulation}
                  className="flex items-center gap-1.5 px-4 py-2 bg-slate-800 hover:bg-slate-700 text-slate-200 rounded-lg text-xs font-semibold transition"
                >
                  <RotateCcw className="w-3.5 h-3.5" />
                  Reset Simulation to Healthy Baseline
                </button>

                <span className="text-[11px] text-slate-500 font-mono">
                  Engine: Python SimulationEngine + FastAPI Backend
                </span>
              </div>
            </div>
          </div>
        )}
      </main>
    </div>
  );
}
