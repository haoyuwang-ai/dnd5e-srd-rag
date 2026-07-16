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
    <main className="min-h-[100dvh] bg-white text-slate-900">
      <div className="mx-auto flex min-h-[100dvh] w-full max-w-3xl flex-col px-4 sm:px-6">
        <header className="flex h-16 shrink-0 items-center justify-between border-b border-slate-200">
          <div className="flex items-center gap-3">
            <div className="flex size-9 items-center justify-center rounded-xl bg-red-600 text-[11px] font-bold tracking-tight text-white shadow-sm">
              D20
            </div>

            <div>
              <h1 className="text-sm font-semibold tracking-tight text-slate-900">
                D&D Rules Chat
              </h1>
              <p className="text-xs text-slate-500">SRD 5.2.1</p>
            </div>
          </div>

          <p className="hidden text-xs text-slate-400 sm:block">
            Rules answers with cited sources
          </p>
        </header>

        <div className="flex flex-1 flex-col py-8 sm:py-12">
          {!answer && !error && !isLoading ? (
            <section className="flex flex-1 flex-col items-center justify-center pb-24 text-center">
              <div className="mb-5 flex size-12 items-center justify-center rounded-2xl border border-red-100 bg-red-50 text-sm font-bold text-red-600">
                20
              </div>

              <h2 className="text-2xl font-semibold tracking-tight text-slate-900 sm:text-3xl">
                What rule are you looking for?
              </h2>

              <p className="mt-3 max-w-md text-sm leading-6 text-slate-500">
                Ask about combat, spells, conditions, character options, or
                other rules covered by the SRD.
              </p>
            </section>
          ) : (
            <div className="flex-1 space-y-8">
              {isLoading && (
                <section
                  aria-live="polite"
                  className="flex items-center gap-3 text-sm text-slate-500"
                >
                  <span className="size-2 animate-pulse rounded-full bg-red-500" />
                  Consulting the rules...
                </section>
              )}

              {error && (
                <div
                  role="alert"
                  className="rounded-2xl border border-red-200 bg-red-50 px-4 py-3 text-sm leading-6 text-red-700"
                >
                  {error}
                </div>
              )}

              {answer && (
                <section aria-labelledby="answer-heading">
                  <div className="flex gap-4">
                    <div className="mt-0.5 flex size-8 shrink-0 items-center justify-center rounded-lg bg-red-600 text-[10px] font-bold text-white">
                      D20
                    </div>

                    <div className="min-w-0 flex-1">
                      <h2
                        id="answer-heading"
                        className="mb-3 text-sm font-semibold text-slate-900"
                      >
                        Rules answer
                      </h2>

                      <p className="whitespace-pre-wrap text-[15px] leading-7 text-slate-700">
                        {answer}
                      </p>
                    </div>
                  </div>
                </section>
              )}

              {answer && (
                <section
                  aria-labelledby="sources-heading"
                  className="border-t border-slate-200 pt-6"
                >
                  <h2
                    id="sources-heading"
                    className="mb-4 text-sm font-semibold text-slate-900"
                  >
                    Sources
                  </h2>

                  {sources.length === 0 ? (
                    <p className="text-sm text-slate-500">
                      No sources were returned.
                    </p>
                  ) : (
                    <ul className="space-y-2">
                      {sources.map((source, index) => (
                        <li
                          key={`${source.label}-${index}`}
                          className="rounded-xl border border-slate-200 bg-slate-50/70 px-4 py-3 transition-colors hover:bg-slate-50"
                        >
                          <p className="text-sm font-medium text-slate-800">
                            {source.label}
                          </p>

                          <dl className="mt-2 flex flex-wrap gap-x-4 gap-y-1 text-xs text-slate-500">
                            <div className="flex gap-1">
                              <dt>Page</dt>
                              <dd className="text-slate-700">
                                {source.page ?? "Unknown"}
                              </dd>
                            </div>

                            <div className="flex gap-1">
                              <dt>Section</dt>
                              <dd className="text-slate-700">
                                {source.section ?? "Unknown"}
                              </dd>
                            </div>

                            <div className="flex gap-1">
                              <dt>Subsection</dt>
                              <dd className="text-slate-700">
                                {source.subsection ?? "Unknown"}
                              </dd>
                            </div>
                          </dl>
                        </li>
                      ))}
                    </ul>
                  )}
                </section>
              )}
            </div>
          )}
        </div>

        <footer className="sticky bottom-0 shrink-0 bg-gradient-to-t from-white via-white to-transparent pb-5 pt-8">
          <form
            onSubmit={handleSubmit}
            className="rounded-2xl border border-slate-200 bg-white p-2 shadow-[0_8px_30px_rgba(15,23,42,0.08)] transition-shadow focus-within:border-red-300 focus-within:ring-4 focus-within:ring-red-50"
          >
            <label htmlFor="rules-question" className="sr-only">
              Ask a D&D rules question
            </label>

            <textarea
              id="rules-question"
              value={question}
              onChange={(event) => setQuestion(event.target.value)}
              placeholder="Ask a D&D rules question..."
              rows={3}
              className="max-h-44 min-h-20 w-full resize-none bg-transparent px-3 py-2 text-[15px] leading-6 text-slate-900 outline-none placeholder:text-slate-400"
            />

            <div className="flex items-center justify-between gap-3 px-1 pb-1">
              <p className="pl-2 text-xs text-slate-400">
                Answers are grounded in SRD 5.2.1
              </p>

              <button
                type="submit"
                disabled={isLoading}
                className="shrink-0 rounded-xl bg-red-600 px-4 py-2 text-sm font-medium text-white transition-colors hover:bg-red-700 active:translate-y-px disabled:cursor-not-allowed disabled:opacity-50"
              >
                {isLoading ? "Asking..." : "Ask"}
              </button>
            </div>
          </form>
        </footer>
      </div>
    </main>
  );
}