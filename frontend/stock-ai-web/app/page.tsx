"use client";

import { useState } from "react";
import ReactMarkdown from "react-markdown";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  CartesianGrid,
} from "recharts";

type Message = {
  role: "user" | "assistant";
  content: string;
};

type StockData = {
  stock_code: string;
  stock_name: string;
  trade_date: string;
  close: number;
  ma5: number;
  ma20: number;
  ma60: number;
  trend_type: string;
  cross_signal: string;
  daily_return: number;
  cumulative_return: number;
};

type RetrievedDoc = {
  source_name: string;
  chunk_text: string;
  distance: number;
};

type ChartData = {
  trade_date: string;
  close: number;
  ma5: number | null;
  ma20: number | null;
  ma60: number | null;
};

export default function Home() {
  const [question, setQuestion] = useState("");
  const [messages, setMessages] = useState<Message[]>([]);
  const [stockData, setStockData] = useState<StockData | null>(null);
  const [docs, setDocs] = useState<RetrievedDoc[]>([]);
  const [chartData, setChartData] = useState<ChartData[]>([]);
  const [loading, setLoading] = useState(false);

  async function fetchChart(stockCode: string) {
    const response = await fetch(
      `http://localhost:8000/stocks/${stockCode}/chart?limit=60`
    );

    const data = await response.json();

    setChartData(data);
  }

  async function handleAsk() {
    if (!question.trim()) return;

    const userMessage: Message = {
      role: "user",
      content: question,
    };

    setMessages((prev) => [...prev, userMessage]);
    setLoading(true);

    try {
      const response = await fetch(
        "http://localhost:8000/rag/chat",
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
      const assistantMessage: Message = {
        role: "assistant",
        content: data.answer,
      };

      setMessages((prev) => [...prev, assistantMessage]);
      setStockData(data.stock_data);
      setDocs(data.retrieved_docs || []);

      if (data.stock_data?.stock_code) {
        await fetchChart(data.stock_data.stock_code);
      }

      setQuestion("");
    } catch (error) {
      console.error(error);

      const errorMessage: Message = {
        role: "assistant",
        content: "Error calling API",
      };

      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="min-h-screen p-10">
      <h1 className="text-5xl font-bold mb-10">
        AI Stock Assistant
      </h1>

      <div className="flex gap-2 mb-6">
        <input
          className="border p-4 w-full text-2xl rounded"
          placeholder="Ask something..."
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
        />

        <button
          onClick={handleAsk}
          className="bg-white text-black px-6 py-4 rounded font-bold"
        >
          Ask
        </button>
      </div>

      {loading && (
        <p className="text-xl mb-4">
          Analyzing technical indicators and searching documents...
        </p>
      )}

      <div className="space-y-4 mt-6">
        {messages.map((message, index) => (
          <div
            key={index}
            className={
              message.role === "user"
                ? "border p-4 rounded bg-gray-900"
                : "border p-6 rounded"
            }
          >
            <p className="font-bold mb-2">
              {message.role === "user" ? "You" : "AI Answer"}
            </p>

            <div className="text-xl leading-relaxed">
              <ReactMarkdown>
                {message.content}
              </ReactMarkdown>
            </div>
          </div>
        ))}
      </div>

      {stockData && (
        <div className="border p-6 rounded mt-6">
          <h2 className="text-3xl font-bold mb-6">
            Technical Indicators
          </h2>

          <div className="grid grid-cols-2 gap-4 text-lg">
            <p>Stock: {stockData.stock_code} {stockData.stock_name}</p>
            <p>Date: {stockData.trade_date}</p>
            <p>Close: {stockData.close}</p>
            <p>MA5: {stockData.ma5}</p>
            <p>MA20: {stockData.ma20}</p>
            <p>MA60: {stockData.ma60}</p>
            <p>Trend: {stockData.trend_type}</p>
            <p>Cross Signal: {stockData.cross_signal}</p>
            <p>Daily Return: {stockData.daily_return}</p>
            <p>Cumulative Return: {stockData.cumulative_return}</p>
          </div>
        </div>
      )}

      {chartData.length > 0 && (
        <div className="border p-6 rounded mt-6">
          <h2 className="text-3xl font-bold mb-6">
            Price & Moving Average Chart
          </h2>

          <div className="w-full h-[400px]">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={chartData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="trade_date" />
                <YAxis />
                <Tooltip />

                <Line
                  type="monotone"
                  dataKey="close"
                  name="Close"
                  stroke="#ffffff"
                  dot={false}
                />

                <Line
                  type="monotone"
                  dataKey="ma5"
                  name="MA5"
                  stroke="#22c55e"
                  dot={false}
                />

                <Line
                  type="monotone"
                  dataKey="ma20"
                  name="MA20"
                  stroke="#3b82f6"
                  dot={false}
                />

                <Line
                  type="monotone"
                  dataKey="ma60"
                  name="MA60"
                  stroke="#f97316"
                  dot={false}
                />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </div>
      )}

      {docs.length > 0 && (
        <div className="border p-6 rounded mt-6">
          <h2 className="text-3xl font-bold mb-6">
            Retrieved Documents
          </h2>

          <div className="space-y-4">
            {docs.map((doc, index) => (
              <div
                key={index}
                className="border p-4 rounded"
              >
                <p className="text-sm opacity-70 mb-2">
                  Source: {doc.source_name}
                </p>

                <p className="text-lg leading-relaxed">
                  {doc.chunk_text}
                </p>

                <p className="text-sm opacity-70 mt-3">
                  Distance: {doc.distance}
                </p>
              </div>
            ))}
          </div>
        </div>
      )}
    </main>
  );
}