"use client";

import { useState } from "react";

export default function Home() {

  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");
  const [loading, setLoading] = useState(false);

  async function handleAsk() {
    if (!question) return;
    setLoading(true);

    try {
      const response = await fetch(
        "http://127.0.0.1:8000/rag/chat",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            question,
          }),
        }
      );

      const data = await response.json();
      console.log(data);
      setAnswer(data.answer);
    } catch (error) {
      console.error(error);
      setAnswer("Error calling API");
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="min-h-screen p-10">

      <h1 className="text-3xl font-bold mb-6">
        AI Stock Assistant
      </h1>

      <div className="flex gap-2 mb-4">

        <input
          className="border p-2 w-full"
          placeholder="Ask something..."
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
        />

        <button
          onClick={handleAsk}
          className="bg-black text-white px-4 py-2"
        >
          Ask
        </button>

      </div>

      {loading && (
        <p>Loading...</p>
      )}

      {answer && (
        <div className="border p-4 rounded">
          <h2 className="font-bold mb-2">
            AI Answer
          </h2>

          <p>{answer}</p>
        </div>
      )}

    </main>
  );
}