export const metadata = { title: "Planet Minutes", description: "Leaders por minutos" };

export default function RootLayout({ children }) {
  return (
    <html lang="pt-br">
      <body style={{ margin:0, fontFamily:"system-ui, sans-serif", background:"#0b0d12", color:"#e6edf3" }}>
        <div style={{ maxWidth:1100, margin:"0 auto", padding:24 }}>
          <div style={{display:"flex", justifyContent:"space-between", alignItems:"center"}}>
            <strong>Planet Minutes</strong>
            <small style={{opacity:.7}}>demo</small>
          </div>
          {children}
        </div>
      </body>
    </html>
  );
}
