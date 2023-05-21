"""
FRANCESC VALERO RIUZ

Sonido estéreo y ficheros WAVE
"""

import wave


def abrir_wave(fichero):
    with wave.open(fichero, 'rb') as archivo_wave:
        parametros = archivo_wave.getparams()
        muestras = archivo_wave.readframes(parametros.nframes)
        return parametros, muestras


def crear_cabecera_wave(sample_rate, num_canales, bits_per_sample, data_size):
    cabecera = wave.open('temp.wav', 'wb')
    cabecera.setnchannels(num_canales)
    cabecera.setsampwidth(bits_per_sample // 8)
    cabecera.setframerate(sample_rate)
    cabecera.setnframes(data_size // (num_canales * (bits_per_sample // 8)))
    cabecera.setcomptype('NONE', 'not compressed')
    return cabecera


def estereo2mono(fichero_entrada, fichero_salida, canal=2):
     
    parametros, muestras = abrir_wave(fichero_entrada)
    num_canales = parametros.nchannels
    muestras_mono = []

    if num_canales == 2:
        for i in range(0, len(muestras), 4):
            muestra = muestras[i:i+4]
            if canal == 0:
                muestras_mono.append(muestra[0:2])
            elif canal == 1:
                muestras_mono.append(muestra[2:4])
            elif canal == 2:
                semisuma = ((muestra[0] + muestra[2]) // 2).to_bytes(2, 'little', signed=True)
                muestras_mono.append(semisuma)
            elif canal == 3:
                semidiferencia = ((muestra[0] - muestra[2]) // 2).to_bytes(2, 'little', signed=True)
                muestras_mono.append(semidiferencia)

    cabecera_mono = crear_cabecera_wave(parametros.framerate, 1, parametros.sampwidth * 8, len(muestras_mono))
    with wave.open(fichero_salida, 'wb') as archivo_salida:
        archivo_salida.setparams(cabecera_mono.getparams())
        archivo_salida.writeframes(b''.join(muestras_mono))


def mono2estereo(fichero_entrada, fichero_salida):

    parametros, muestras = abrir_wave(fichero_entrada)

    muestras_estereo = []
    for i in range(0, len(muestras), 2):
        muestra = muestras[i:i+2]
        muestras_estereo.extend(muestra * 2)

    cabecera_estereo = crear_cabecera_wave(parametros.framerate, 2, parametros.sampwidth * 8, len(muestras_estereo))
    with wave.open(fichero_salida, 'wb') as archivo_salida:
        archivo_salida.setparams(cabecera_estereo.getparams())
        archivo_salida.writeframes(b''.join(muestras_estereo))


def codEstereo(fichero_entrada, fichero_salida):

    parametros, muestras = abrir_wave(fichero_entrada)

    muestras_codificadas = []
    for i in range(0, len(muestras), 2):
        muestra = muestras[i:i+2]
        muestra_codificada = (muestra[0] ^ muestra[1]).to_bytes(2, 'little')
        muestras_codificadas.append(muestra_codificada)

    cabecera_codificada = crear_cabecera_wave(parametros.framerate, parametros.nchannels, parametros.sampwidth * 8, len(muestras_codificadas))
    with wave.open(fichero_salida, 'wb') as archivo_salida:
        archivo_salida.setparams(cabecera_codificada.getparams())
        archivo_salida.writeframes(b''.join(muestras_codificadas))


def decEstereo(fichero_entrada, fichero_salida):

    parametros, muestras = abrir_wave(fichero_entrada)

    muestras_decodificadas = []
    for i in range(0, len(muestras), 2):
        muestra = muestras[i:i+2]
        muestra_decodificada = (muestra[0] ^ muestra[1]).to_bytes(2, 'little')
        muestras_decodificadas.append(muestra_decodificada)

    cabecera_decodificada = crear_cabecera_wave(parametros.framerate, parametros.nchannels, parametros.sampwidth * 8, len(muestras_decodificadas))
    with wave.open(fichero_salida, 'wb') as archivo_salida:
        archivo_salida.setparams(cabecera_decodificada.getparams())
        archivo_salida.writeframes(b''.join(muestras_decodificadas))
