class Library {
    constructor() {
        this.libros = [];
        this.miembros = [];
        this.reservas = new Map();
        this.prestamos = [];
    }

    agregarLibro(libro) {
        if (this.libros.some((existente) => existente.isbn === libro.isbn))
            throw new Error("El libro ya está registrado.");
        this.libros.push(libro);
    }

    agregarMiembro(miembro) {
        if (this.miembros.some((existente) => existente.id === miembro.id))
            throw new Error("El miembro ya está registrado.");
        this.miembros.push(miembro);
    }

    obtenerMiembroRegistrado(id) {
        const miembro = this.miembros.find((m) => m.id === id);
        if (!miembro) throw new Error("El miembro no está registrado.");
        return miembro;
    }

    obtenerLibroRegistrado(isbn) {
        const libro = this.libros.find((l) => l.isbn === isbn);
        if (!libro) throw new Error("El libro no está registrado.");
        return libro;
    }

    pedirLibro(idMiembro, isbn, fechaPrestamo = new Date()) {
        const miembro = this.obtenerMiembroRegistrado(idMiembro);
        const libro = this.obtenerLibroRegistrado(isbn);

        if (!libro.estaDisponible())
            throw new Error("No hay más libros disponibles");
        if (!miembro.puedePedir())
            throw new Error("El miembro no puede tener más libros que su límite.");

        const [primero] = this.obtenerReservas(isbn);
        if (primero !== undefined && primero !== miembro.id)
            throw new Error("El libro está reservado para otro miembro.");
        libro.pedir();
        miembro.pedir(isbn);
        this.reservas.set(isbn, this.obtenerReservas(isbn).filter((id) => id !== miembro.id));
        this.prestamos.push({ idMiembro, isbn, fechaPrestamo });
        return true;
    }

    regresarLibro(idMiembro, isbn) {
        const miembro = this.obtenerMiembroRegistrado(idMiembro);
        const libro = this.obtenerLibroRegistrado(isbn);
        miembro.regresar(isbn);
        libro.regresar();
        const [siguiente] = this.obtenerReservas(isbn);
        if (siguiente !== undefined)
            this.obtenerMiembroRegistrado(siguiente).notificar(
                `El libro "${libro.titulo}" ya está disponible.`,
            );
        return true;
    }

    buscarPorTitulo(titulo) {
        const texto = titulo.toLowerCase();
        return this.libros.filter((libro) =>
            libro.titulo.toLowerCase().includes(texto),
        );
    }

    buscarPorAutor(autor) {
        const texto = autor.toLowerCase();
        return this.libros.filter((libro) =>
            libro.autor.toLowerCase().includes(texto),
        );
    }
    librosDisponibles() {
        return this.libros.filter((libro) => libro.estaDisponible());
    }

    reservarLibro(idMiembro, isbn) {
        const miembro = this.obtenerMiembroRegistrado(idMiembro);
        const libro = this.obtenerLibroRegistrado(isbn);
        const cola = this.reservas.get(isbn) ?? [];

        if (cola.includes(miembro.id))
            throw new Error("El miembro ya tiene una reserva para este libro.");
        if (libro.estaDisponible())
            throw new Error("El libro está disponible, no necesita reserva.");

        cola.push(miembro.id);
        this.reservas.set(isbn, cola);
        return cola.length;
    }

    obtenerReservas(isbn) {
        return [...(this.reservas.get(isbn) ?? [])];
    }

    quitarReserva(isbn, idMiembro) {
        this.reservas.set(isbn, this.obtenerReservas(isbn).filter((id) => id !== idMiembro));
    }

    notificarSiguienteEnCola(libro) {
        const [siguiente] = this.obtenerReservas(libro.isbn);
        if (siguiente === undefined) return;
        this.obtenerMiembroRegistrado(siguiente).notificar(
            `El libro "${libro.titulo}" ya está disponible.`,
        );
    }

    fechaVencimiento(idMiembro, isbn) {
        if (!prestamo)
            throw new Error("El miembro no tiene prestado este libro.");
        const prestamo = this.prestamos.find(
            (p) => p.idMiembro === idMiembro && p.isbn === isbn,
        );
        return new Date(prestamo.fechaPrestamo.getTime() + 14 * 24 * 60 * 60 * 1000);
    }

    calcularRecargo(idMiembro, isbn, fechaActual = new Date()) {
        const vencimiento = this.fechaVencimiento(idMiembro, isbn);
        const dias = Math.max(0, Math.floor((fechaActual - vencimiento) / (24 * 60 * 60 * 1000)));
        return dias * 1;
    }
}

module.exports = { Library };
