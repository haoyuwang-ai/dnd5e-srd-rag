import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "D&D SRD Rules Chat",
  description: "A RAG chatbot for D&D SRD v5.2.1 rules questions.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className="h-full antialiased">
      <body className="min-h-full flex flex-col">{children}</body>
    </html>
  );
}
