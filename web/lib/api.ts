export type SourceItem = {
  label: string;
  page: number | null;
  section: string | null;
  subsection: string | null;
};

export type ChatResponse = {
  answer: string;
  sources: SourceItem[];
};

export async function askSrd(question: string): Promise<ChatResponse> {
  const baseUrl = process.env.NEXT_PUBLIC_API_BASE_URL;

  if (!baseUrl) {
    throw new Error("NEXT_PUBLIC_API_BASE_URL is not set.");
  }

  const response = await fetch(`${baseUrl}/api/chat`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      question,
      top_k: 5,
      
    }),
  });

  const data = await response.json();

  if (!response.ok) {
    throw new Error(data.detail ?? "Failed to ask SRD API.");
  }

  return data;
}