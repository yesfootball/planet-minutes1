"use client";
import { useEffect, useState } from "react";
import { getJSON } from "../../lib/api";
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer } from "recharts";

export default function Page() {
  const [competitionId, setCompetitionId] = useState(1);
  const [data, setData] = useState([]);
  const [err, setErr] = useState(null);

  useEffect(() => {
    (async () => {
      try {
        setErr(null);
        const res = await getJSON(`/competitions/${competitionId}/leaders`);
        setData(res.slice(0, 10));
      } catch (e) {
        setErr(String(e));
      }
    })();
  }, [competitionId]);

  return (
    <div>
      <h2>Leaders por Minutos</h2>
      <div style={{display:"flex", gap:8, alignItems:"center"}}>
        <label>Competition ID</label>
        <input type="number" value={competitionId} onChange={e => setCompetitionId(parseInt(e.target.value||"0",10))} />
      </div>

      <div style={{background:"#111521", border:"1px solid #1c2233", borderRadius:16, padding:18, marginTop:16}}>
        {err && <div style={{color:"#f66"}}>Erro: {err}</div>}
        {!err && data.length === 0 && <div>Sem dados — rode o seed.</div>}
        {data.length > 0 && (
          <div style={{width:"100%", height:360}}>
            <ResponsiveContainer>
              <BarChart data={data}>
                <XAxis dataKey="player" interval={0} tick={{fontSize:12}} />
                <YAxis />
                <Tooltip />
                <Bar dataKey="minutes_total" />
              </BarChart>
            </ResponsiveContainer>
          </div>
        )}
      </div>
    </div>
  );
}
