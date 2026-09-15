@extends('layouts.app')

@section('title', 'Contenido')

@section('content')
    <section class="py-8 text-center sm:py-12">
        <h1 class="page-title">
            Descubre el contenido disponible
        </h1>

        <p class="page-description mx-auto">
            Consulta novedades, recursos y espacios de comunidad desde una
            interfaz simple, clara y adaptable a dispositivos móviles.
        </p>
    </section>

    <section
        class="grid gap-5 pb-10 md:grid-cols-2 lg:grid-cols-3"
        aria-label="Secciones de contenido"
    >
        @foreach ($contents as $content)
            <article class="content-card flex min-h-60 flex-col">
                <span class="content-badge self-start">
                    {{ $content['label'] }}
                </span>

                <h2 class="mt-5 text-xl font-bold text-slate-900">
                    {{ $content['title'] }}
                </h2>

                <p class="mt-3 leading-7 text-slate-600">
                    {{ $content['description'] }}
                </p>

                <a
                    href="#"
                    class="mt-auto pt-6 font-semibold text-rose-600 hover:text-rose-700"
                    aria-label="Ver {{ $content['title'] }}"
                >
                    Ver más →
                </a>
            </article>
        @endforeach
    </section>

    <section class="mb-10 rounded-2xl bg-gradient-to-br from-rose-600 to-rose-900 px-6 py-10 text-center text-white">
        <h2 class="text-2xl font-bold">
            ¿Listo para explorar?
        </h2>

        <p class="mx-auto mt-3 max-w-2xl leading-7 text-rose-100">
            Esta sección puede crecer después con contenido proveniente de una
            base de datos, un panel administrativo o una API.
        </p>

        <a
            href="{{ route('content.index') }}"
            class="mt-6 inline-flex rounded-lg bg-white px-4 py-2 font-semibold text-rose-700 transition hover:bg-rose-50"
        >
            Explorar contenido
        </a>
    </section>
@endsection