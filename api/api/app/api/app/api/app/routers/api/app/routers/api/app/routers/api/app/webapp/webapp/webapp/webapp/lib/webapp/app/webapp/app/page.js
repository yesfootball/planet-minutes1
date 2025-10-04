import Link from "next/link";
export default function Page() {
  return (
    <div style={{padding:"48px 0", textAlign:"center"}}>
      <h1>Minutes that matter</h1>
      <p>Veja líderes por minutos jogados por competição.</p>
      <Link href="/dashboard" style={{background:"#6ea8fe", color:"#0b0d12", padding:"12px 18px", borderRadius:12, fontWeight:700}}>Abrir Dashboard</Link>
    </div>
  );
}
