<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">

    <title>@yield('title', 'Mi aplicación')</title>

    @vite(['resources/css/app.css', 'resources/js/app.js'])
</head>
<body class="min-h-screen bg-slate-50 font-sans text-slate-900">
    <header class="border-b border-slate-200 bg-white">
        <nav class="mx-auto flex max-w-6xl items-center justify-between px-6 py-4">
            <a href="{{ url('/') }}" class="text-lg font-bold text-rose-600">
                Mi Aplicación
            </a>

            <a
                href="{{ url('/') }}"
                class="text-sm font-semibold text-slate-600 transition hover:text-rose-600"
            >
                Inicio
            </a>
        </nav>
    </header>

    <main class="mx-auto w-full max-w-6xl px-6 py-10">
        @yield('content')
    </main>
</body>
</html>