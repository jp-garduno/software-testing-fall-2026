class Utils {
  static min = 0;
  static max = 100;

  static cambiarNum(value) {
    if (value < Utils.min) return Utils.min;
    if (value > Utils.max) return Utils.max;
    return value;
  }

  static cambiarColor(value) {
    if (value < 33) return 'rojo';
    if (value < 66) return 'amarillo';
    return 'verde';
  }
}

module.exports = { Utils };

// fn + f2
