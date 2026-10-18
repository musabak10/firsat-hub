import type { Metadata } from "next";
import Link from "next/link";
import { Public_Sans } from "next/font/google";
import "./globals.css";

const sans = Public_Sans({ subsets: ["latin", "latin-ext"], variable: "--font-sans" });

export const metadata: Metadata = {
  title: { default: "Fırsat Hub – Öğrenciler için staj, hackathon ve yarışmalar", template: "%s | Fırsat Hub" },
  description: "Lise ve üniversite öğrencileri için ücretsiz staj, hackathon, yarışma, boot-camp ve konferansları tek yerde bul.",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="tr" className={sans.variable}>
      <body className="font-sans antialiased">
        <header className="border-b border-slate-200 bg-white">
          <div className="mx-auto flex max-w-6xl items-center justify-between px-4 py-4">
            <Link href="/" className="text-lg font-semibold text-navy-900">Fırsat Hub</Link>
            <span className="text-sm text-slate-500">Öğrenci etkinlikleri</span>
          </div>
        </header>
        <main className="mx-auto max-w-6xl px-4 py-8">{children}</main>
        <footer className="mx-auto flex max-w-6xl flex-col items-center justify-between gap-4 border-t border-slate-100 px-4 py-8 text-sm text-slate-500 sm:flex-row">
          <span>Başvurmadan önce son tarihi etkinliğin resmi sayfasından doğrulayın.</span>
          <span>
            İletişim:{" "}
            <a
              href="mailto:musabakten070@gmail.com"
              className="font-medium text-slate-700 underline transition hover:text-slate-900"
            >
              musabakten070@gmail.com
            </a>
          </span>
        </footer>
      </body>
    </html>
  );
}
