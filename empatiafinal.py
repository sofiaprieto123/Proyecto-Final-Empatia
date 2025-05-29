''' Universidad del valle de guatemala
Algoritmos y programacion basica
Sofia prieto #25654, Alejandro aldana #25249, Adrián Chacón #25296, Jose Menegazzo #251437 '''

import streamlit as st
import json
import os
st.set_page_config(page_title="SYNK", page_icon="💙", layout="centered")

st.markdown(
    """
    <style>
    /* Fondo general y texto */
    .stApp {
        background-color: #0d1b2a;
        color: white;
    }

    /* Título grande centrado */
    h1 {
        text-align: center;
        color: #ffffff;
        font-family: 'Trebuchet MS', sans-serif;
    }

    /* Botones personalizados */
    .stButton>button {
        background-color: #1b6ca8;
        color: white;
        border-radius: 8px;
        padding: 0.6em 1.5em;
        border: none;
        font-size: 16px;
    }

    .stButton>button:hover {
        background-color: #14507a;
        color: #fff;
        cursor: pointer;
    }

    /* Inputs de texto y selects */
    input, textarea, select {
        background-color: #f0f4f8;
        color: #000;
        border-radius: 6px;
        padding: 6px;
    }

    /* Responsive: textos e inputs más grandes en móvil */
    @media only screen and (max-width: 768px) {
        .stApp {
            padding: 1rem;
        }

        h1 {
            font-size: 28px;
        }

        .stButton>button {
            font-size: 14px;
            padding: 0.5em 1.2em;
        }
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown("<h1>SYNK</h1>", unsafe_allow_html=True)
# Ruta del archivo de usuarios
FILE_PATH = "usuarios.json"

# Crear archivo de usuarios si no existe
if not os.path.exists(FILE_PATH):
    with open(FILE_PATH, "w") as f:
        json.dump({"usuario1": "clave123", "admin": "adminpass"}, f)

# Funciones de manejo de usuarios
def cargar_usuarios():
    if os.path.exists(FILE_PATH):
        with open(FILE_PATH, "r") as f:
            contenido = f.read().strip()
            if contenido:
                try:
                    return json.loads(contenido)
                except json.JSONDecodeError:
                    st.warning("El archivo de usuarios está corrupto. Se reiniciará.")
    # Crear datos por defecto si no hay contenido válido
    usuarios_por_defecto = {"usuario1": "clave123", "admin": "adminpass"}
    guardar_usuarios(usuarios_por_defecto)
    return usuarios_por_defecto

def guardar_usuarios(usuarios):
    with open(FILE_PATH, "w") as f:
        json.dump(usuarios, f)

usuarios = cargar_usuarios()

# Inicializar estados
for key in [
    "logueado", "usuario", "plan_seleccionado", "tipo_relacion",
    "mostrar_opciones", "valores_respondidos", "valores_seleccionados",
    "registro_activo"
]:
    if key not in st.session_state:
        st.session_state[key] = False if key.startswith("mostrar") or key.endswith("respondidos") else None

# -----------------------
# LOGIN O REGISTRO
# -----------------------
if not st.session_state.logueado:
    st.title("Bienvenido")

    st.session_state.registro_activo = st.radio("¿Tienes una cuenta o deseas registrarte?", ["Iniciar sesión", "Crear cuenta"]) == "Crear cuenta"

    if st.session_state.registro_activo:
        st.subheader("Crear Cuenta Nueva")
        nuevo_usuario = st.text_input("Nuevo Usuario")
        nueva_clave = st.text_input("Nueva Contraseña", type="password")

        if st.button("Registrar"):
            if nuevo_usuario in usuarios:
                st.error("El usuario ya existe.")
            elif nuevo_usuario == "" or nueva_clave == "":
                st.error("Usuario y contraseña no pueden estar vacíos.")
            else:
                usuarios[nuevo_usuario] = nueva_clave
                guardar_usuarios(usuarios)
                st.success("Usuario registrado exitosamente. Ahora puedes iniciar sesión.")

    else:
        st.subheader("Iniciar Sesión")
        usuario = st.text_input("Usuario")
        clave = st.text_input("Contraseña", type="password")

        if st.button("Entrar"):
            if usuario in usuarios and usuarios[usuario] == clave:
                st.session_state.logueado = True
                st.session_state.usuario = usuario
                st.success(f"Bienvenido, {usuario}")
            else:
                st.error("Usuario o contraseña incorrectos.")

# -----------------------
# BOTÓN CERRAR SESIÓN
# -----------------------
if st.session_state.logueado:
    if st.button("Cerrar sesión"):
        for key in st.session_state.keys():
            st.session_state[key] = False if isinstance(st.session_state[key], bool) else None
        st.rerun()

# -----------------------
# ENCUESTA DE VALORES
# -----------------------
if st.session_state.logueado and not st.session_state.valores_respondidos:
    st.title("Encuesta de Valores Personales")
    valores = ["Familia", "Amigos", "Dinero", "Sinceridad", "Confianza", "Compromiso", "Respeto"]
    seleccionados = st.multiselect("¿Cuáles de estos valores son importantes para ti?", valores)

    if st.button("Continuar"):
        st.session_state.valores_respondidos = True
        st.session_state.valores_seleccionados = seleccionados
        if seleccionados:
            st.success(f"Has seleccionado: {', '.join(seleccionados)}")
        else:
            st.info("No seleccionaste ningún valor. Puedes continuar.")

# -----------------------
# MENÚ DE PLANES
# -----------------------
if st.session_state.valores_respondidos:
    st.title("Menú de Planes")

    plan = st.radio("¿Qué plan desea consumir?", ["Plan Común", "Plan Premium", "Salir"])

    if plan == "Salir":
        st.session_state.mostrar_opciones = False
        st.info("¡Gracias por usar nuestro servicio!")
    else:
        tipo = st.radio("¿Qué tipo de relación desea establecer?", ["pareja", "amistosa"])

        if st.button("Confirmar selección"):
            st.session_state.plan_seleccionado = plan
            st.session_state.tipo_relacion = tipo
            st.session_state.mostrar_opciones = True

# -----------------------
# OPCIONES DEL PLAN
# -----------------------
if st.session_state.mostrar_opciones:
    tipo = st.session_state.tipo_relacion
    plan = st.session_state.plan_seleccionado

    if plan == "Plan Común":
        if tipo == "pareja":
            flores = ["Ramo de rosas", "Tulipanes"]
            postres = ["Cupcakes", "Galletas artesanales"]
        else:
            flores = ["Girasoles", "Daisies"]
            postres = ["Brownies", "Muffins"]

        flor = st.selectbox("Seleccione una flor:", flores)
        postre = st.selectbox("Seleccione un postre:", postres)

        if st.button("Confirmar selección del Plan Común"):
            st.success(f"Has seleccionado: {flor} y {postre} para una relación de tipo {tipo}.")

    elif plan == "Plan Premium":
        if tipo == "pareja":
            flores = ["Ramo deluxe de rosas y lirios", "Caja floral romántica"]
            postres = ["Tarta gourmet", "Cheesecake artesanal"]
            restaurantes = ["Narù", "Biba"]
        else:
            flores = ["Caja floral premium", "Centro de mesa elegante"]
            postres = ["Macaroons importados", "Mousse de chocolate"]
            restaurantes = ["Le Café", "Saúl"]

        flor = st.selectbox("Seleccione una flor:", flores)
        postre = st.selectbox("Seleccione un postre:", postres)
        restaurante = st.selectbox("Seleccione un restaurante:", restaurantes)

        if st.button("Confirmar selección del Plan Premium"):
            st.success(f"Has seleccionado: {flor}, {postre} y una cena en {restaurante} para una relación de tipo {tipo}.")

# -----------------------
# MOSTRAR VALORES SELECCIONADOS
# -----------------------
if st.session_state.valores_respondidos and st.session_state.valores_seleccionados is not None:
    with st.expander("Ver valores personales seleccionados"):
        if st.session_state.valores_seleccionados:
            st.write("Tus valores importantes son:")
            for val in st.session_state.valores_seleccionados:
                st.markdown(f"- {val}")
        else:
            st.write("No seleccionaste ningún valor.")