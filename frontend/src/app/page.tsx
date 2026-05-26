import Link from "next/link";

export default function Home() {
  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-gradient-to-br from-sky-50 to-emerald-50">
      <div className="text-center max-w-2xl px-4">
        <h1 className="text-5xl font-bold text-gray-900 mb-4">
          AI-Powered <span className="text-sky-500">Health Tracker</span>
        </h1>
        <p className="text-lg text-gray-600 mb-8">
          Track your daily health metrics, get AI-powered insights, and generate PDF reports for your doctor.
        </p>
        <div className="flex gap-4 justify-center">
          <Link href="/login" className="px-6 py-3 bg-sky-500 text-white rounded-lg font-medium hover:bg-sky-600 transition">
            Sign In
          </Link>
          <Link href="/register" className="px-6 py-3 border border-sky-500 text-sky-500 rounded-lg font-medium hover:bg-sky-50 transition">
            Create Account
          </Link>
        </div>
        <div className="grid grid-cols-3 gap-6 mt-16 text-left">
          {[
            { title: "Track Metrics", desc: "Weight, BP, sleep, mood, steps & more" },
            { title: "AI Insights", desc: "Anomaly detection, correlations & Q&A" },
            { title: "PDF Reports", desc: "Shareable reports for your healthcare provider" },
          ].map((f) => (
            <div key={f.title} className="bg-white p-4 rounded-lg shadow-sm">
              <h3 className="font-semibold text-gray-900">{f.title}</h3>
              <p className="text-sm text-gray-500 mt-1">{f.desc}</p>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
