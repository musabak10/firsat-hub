import Link from "next/link";
export default function NotFound() {
  return (
    <div className="py-20 text-center">
      <h1 className="text-2xl font-semibold text-navy-900">Etkinlik bulunamadı</h1>
      <p className="mt-2 text-slate-600">Kaldırılmış veya henüz yayına alınmamış olabilir.</p>
      <Link href="/" className="mt-6 inline-block text-steel-600 hover:underline">Tüm etkinliklere dön</Link>
    </div>
  );
}
