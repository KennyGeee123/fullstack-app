export default function Home() {
  return (
    <main className="min-h-screen bg-black text-white flex flex-col items-center justify-center gap-8 p-8">
      <div className="text-center">
        <h1 className="text-5xl font-bold tracking-tight mb-3">Fullstack App</h1>
        <p className="text-zinc-400 text-lg">Autonomous deploy pipeline active</p>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 w-full max-w-2xl">
        <StatusCard label="CI/CD" value="Active" color="green" />
        <StatusCard label="Auto-sync" value="Running" color="green" />
        <StatusCard label="Deploy" value="Vercel" color="blue" />
      </div>

      <a
        href="/api/status"
        className="text-sm text-zinc-500 hover:text-white transition-colors"
      >
        /api/status →
      </a>
    </main>
  );
}

function StatusCard({
  label,
  value,
  color,
}: {
  label: string;
  value: string;
  color: "green" | "blue";
}) {
  const dot = color === "green" ? "bg-green-400" : "bg-blue-400";
  return (
    <div className="border border-zinc-800 rounded-xl p-4 flex flex-col gap-2">
      <span className="text-zinc-500 text-sm">{label}</span>
      <div className="flex items-center gap-2">
        <span className={`w-2 h-2 rounded-full ${dot} animate-pulse`} />
        <span className="font-medium">{value}</span>
      </div>
    </div>
  );
}
