"use client";

import { useState, type FormEvent } from "react";
import { askSrd, type SourceItem } from "@/lib/api";

export default function Home() {
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");
  const [sources, setSources] = useState<SourceItem[]>([]);
  const [error, setError] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();

    if (!question.trim()) {
      return;
    }

    setIsLoading(true);
    setError("");
    setAnswer("");
    setSources([]);

    try {
      const result = await askSrd(question);

      setAnswer(result.answer);
      setSources(result.sources);
    } catch (err) {
      if (err instanceof Error) {
        setError(err.message);
      } else {
        setError("Something went wrong.");
      }
    } finally {
      setIsLoading(false);
    }
  }

  return (
    <main className="min-h-screen bg-zinc-950 px-6 py-10 text-zinc-100">
      <div className="mx-auto max-w-3xl">
        
        <header className="mb-8">
          <p className="mb-2 text-sm uppercase tracking-wide text-red-400">
            SRD v5.2.1 RAG
          </p>
          <h1 className="text-3xl font-semibold tracking-tight">
            D&D Rules Chat
          </h1>
          <p className="mt-2 text-sm text-zinc-400">
            Ask rules questions and get answers with page-backed SRD sources.
          </p>
        </header>

        <form onSubmit={handleSubmit} className="mb-8 flex gap-3">
          <textarea
            value={question}
            onChange={(event) => setQuestion(event.target.value)}
            placeholder="Ask a D&D SRD question..."
            rows={3}
            className="min-h-24 flex-1 resize-none rounded-lg border border-zinc-700 bg-zinc-900 px-4 py-3 text-sm text-zinc-100 outline-none focus:border-red-500"
          />

          <button
            type="submit"
            disabled={isLoading}
            className="rounded-lg bg-red-700 px-5 py-3 text-sm font-medium text-white hover:bg-red-600 disabled:cursor-not-allowed disabled:opacity-50"
          >
            {isLoading ? "Asking..." : "Ask"}
          </button>
        </form>

        {error && (
          <div className="mb-6 rounded-lg border border-red-800 bg-red-950 p-4 text-sm text-red-200">
            {error}
          </div>
        )}

        <section className="mb-6 rounded-xl border border-zinc-800 bg-zinc-900 p-5">
          <h2 className="mb-2 text-lg font-semibold">Answer:</h2>
          <p className="whitespace-pre-wrap text-sm leading-7 text-zinc-200">
            {answer || "No answer yet."}
          </p>
        </section>

        <section className="rounded-xl border border-zinc-800 bg-zinc-900 p-5">
          <h2 className="mb-2 text-lg font-semibold">Sources:</h2>

          {sources.length === 0 ? (
            <p className="text-sm text-zinc-500">No sources yet.</p>
          ) : (
            <ul className="space-y-2">
              {sources.map((source, index) => (
                <li
                  key={`${source.label}-${index}`}
                  className="rounded-lg border border-zinc-800 bg-zinc-950 p-4"
                >
                  <div className="text-sm font-medium text-zinc-100">{source.label}</div>
                  <div className="mt-2 text-xs text-zinc-500">
                    Page: {source.page ?? "unknown"} | Section:{" "}
                    {source.section ?? "unknown"} | Subsection:{" "}
                    {source.subsection ?? "unknown"}
                  </div>
                </li>
              ))}
            </ul>
          )}
        </section>
      </div>
    </main>
  );
}
