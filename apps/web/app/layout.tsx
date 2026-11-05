import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "AMR Sentinel AI — Clinical Antimicrobial Prescription Auditing",
  description: "Clinician-assistive antimicrobial prescription auditing & stewardship platform",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className="min-h-screen bg-canvas text-ink antialiased">
        {children}
      </body>
    </html>
  );
}
