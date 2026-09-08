<?php

namespace App\Http\Controllers;

use Illuminate\View\View;

class ContentController extends Controller
{
    public function index(): View
    {
        $contents = [
            [
                'title' => 'Novedades',
                'description' => 'Explora las últimas actualizaciones, anuncios y contenido disponible en la plataforma.',
                'label' => 'Actualizado',
            ],
            [
                'title' => 'Recursos',
                'description' => 'Encuentra material útil para consultar, aprender y aprovechar mejor la aplicación.',
                'label' => 'Recomendado',
            ],
            [
                'title' => 'Comunidad',
                'description' => 'Conecta con otros usuarios y mantente al tanto de las actividades importantes.',
                'label' => 'Nuevo',
            ],
        ];

        return view('content.index', compact('contents'));
    }
}