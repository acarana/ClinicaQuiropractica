PGDMP                         x            Clinica    12.2    12.2 "    7           0    0    ENCODING    ENCODING        SET client_encoding = 'UTF8';
                      false            8           0    0 
   STDSTRINGS 
   STDSTRINGS     (   SET standard_conforming_strings = 'on';
                      false            9           0    0 
   SEARCHPATH 
   SEARCHPATH     8   SELECT pg_catalog.set_config('search_path', '', false);
                      false            :           1262    16847    Clinica    DATABASE     �   CREATE DATABASE "Clinica" WITH TEMPLATE = template0 ENCODING = 'UTF8' LC_COLLATE = 'English_United States.1252' LC_CTYPE = 'English_United States.1252';
    DROP DATABASE "Clinica";
                postgres    false            �            1259    16927 	   historial    TABLE     S   CREATE TABLE public.historial (
    paciente_id integer,
    reporte_id integer
);
    DROP TABLE public.historial;
       public         heap    postgres    false            �            1259    16947 
   inventario    TABLE     �   CREATE TABLE public.inventario (
    inventario_id integer NOT NULL,
    articulo character varying(20) NOT NULL,
    cantidad integer NOT NULL,
    CONSTRAINT articulo_positivo CHECK ((cantidad >= 0))
);
    DROP TABLE public.inventario;
       public         heap    postgres    false            �            1259    16945    inventario_inventario_id_seq    SEQUENCE     �   CREATE SEQUENCE public.inventario_inventario_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 3   DROP SEQUENCE public.inventario_inventario_id_seq;
       public          postgres    false    208            ;           0    0    inventario_inventario_id_seq    SEQUENCE OWNED BY     ]   ALTER SEQUENCE public.inventario_inventario_id_seq OWNED BY public.inventario.inventario_id;
          public          postgres    false    207            �            1259    16963    material_cantidad    VIEW     x   CREATE VIEW public.material_cantidad AS
 SELECT inventario.articulo,
    inventario.cantidad
   FROM public.inventario;
 $   DROP VIEW public.material_cantidad;
       public          postgres    false    208    208            �            1259    16874    paciente    TABLE     j  CREATE TABLE public.paciente (
    paciente_id integer NOT NULL,
    nombre character varying(20) NOT NULL,
    apellido character varying(20) NOT NULL,
    fecha_nacimiento date NOT NULL,
    telefono character varying(20) NOT NULL,
    direccion character varying(200),
    CONSTRAINT paciente_telefono_check CHECK (((telefono)::text !~~ '%[^0-9]%'::text))
);
    DROP TABLE public.paciente;
       public         heap    postgres    false            �            1259    16959    paciente_especifico    VIEW     w  CREATE VIEW public.paciente_especifico AS
 SELECT paciente.paciente_id,
    paciente.nombre,
    paciente.apellido,
    paciente.fecha_nacimiento,
    paciente.telefono,
    paciente.direccion
   FROM public.paciente
  WHERE (((paciente.nombre)::text = 'Juan'::text) AND ((paciente.apellido)::text = 'Franceschi'::text) AND ((paciente.telefono)::text = '7876437561'::text));
 &   DROP VIEW public.paciente_especifico;
       public          postgres    false    203    203    203    203    203    203            �            1259    16872    paciente_paciente_id_seq    SEQUENCE     �   CREATE SEQUENCE public.paciente_paciente_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 /   DROP SEQUENCE public.paciente_paciente_id_seq;
       public          postgres    false    203            <           0    0    paciente_paciente_id_seq    SEQUENCE OWNED BY     U   ALTER SEQUENCE public.paciente_paciente_id_seq OWNED BY public.paciente.paciente_id;
          public          postgres    false    202            �            1259    16918    reporte    TABLE     �   CREATE TABLE public.reporte (
    reporte_id integer NOT NULL,
    fecha_creado date NOT NULL,
    nota character varying(500)
);
    DROP TABLE public.reporte;
       public         heap    postgres    false            �            1259    16916    reporte_reporte_id_seq    SEQUENCE     �   CREATE SEQUENCE public.reporte_reporte_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 -   DROP SEQUENCE public.reporte_reporte_id_seq;
       public          postgres    false    205            =           0    0    reporte_reporte_id_seq    SEQUENCE OWNED BY     Q   ALTER SEQUENCE public.reporte_reporte_id_seq OWNED BY public.reporte.reporte_id;
          public          postgres    false    204            �            1259    16955    reportes_paciente    VIEW       CREATE VIEW public.reportes_paciente AS
 SELECT reporte.reporte_id,
    reporte.fecha_creado,
    reporte.nota
   FROM public.reporte
  WHERE (reporte.reporte_id IN ( SELECT historial.reporte_id
           FROM public.historial
          WHERE (historial.paciente_id = ( SELECT paciente.paciente_id
                   FROM public.paciente
                  WHERE (((paciente.nombre)::text = 'Juan'::text) AND ((paciente.apellido)::text = 'Franceschi'::text) AND ((paciente.telefono)::text = '7876437561'::text))))));
 $   DROP VIEW public.reportes_paciente;
       public          postgres    false    206    205    205    206    203    203    203    203    205            �
           2604    16950    inventario inventario_id    DEFAULT     �   ALTER TABLE ONLY public.inventario ALTER COLUMN inventario_id SET DEFAULT nextval('public.inventario_inventario_id_seq'::regclass);
 G   ALTER TABLE public.inventario ALTER COLUMN inventario_id DROP DEFAULT;
       public          postgres    false    208    207    208            �
           2604    16877    paciente paciente_id    DEFAULT     |   ALTER TABLE ONLY public.paciente ALTER COLUMN paciente_id SET DEFAULT nextval('public.paciente_paciente_id_seq'::regclass);
 C   ALTER TABLE public.paciente ALTER COLUMN paciente_id DROP DEFAULT;
       public          postgres    false    202    203    203            �
           2604    16921    reporte reporte_id    DEFAULT     x   ALTER TABLE ONLY public.reporte ALTER COLUMN reporte_id SET DEFAULT nextval('public.reporte_reporte_id_seq'::regclass);
 A   ALTER TABLE public.reporte ALTER COLUMN reporte_id DROP DEFAULT;
       public          postgres    false    204    205    205            2          0    16927 	   historial 
   TABLE DATA           <   COPY public.historial (paciente_id, reporte_id) FROM stdin;
    public          postgres    false    206   �*       4          0    16947 
   inventario 
   TABLE DATA           G   COPY public.inventario (inventario_id, articulo, cantidad) FROM stdin;
    public          postgres    false    208   !+       /          0    16874    paciente 
   TABLE DATA           h   COPY public.paciente (paciente_id, nombre, apellido, fecha_nacimiento, telefono, direccion) FROM stdin;
    public          postgres    false    203   {+       1          0    16918    reporte 
   TABLE DATA           A   COPY public.reporte (reporte_id, fecha_creado, nota) FROM stdin;
    public          postgres    false    205   c-       >           0    0    inventario_inventario_id_seq    SEQUENCE SET     J   SELECT pg_catalog.setval('public.inventario_inventario_id_seq', 4, true);
          public          postgres    false    207            ?           0    0    paciente_paciente_id_seq    SEQUENCE SET     G   SELECT pg_catalog.setval('public.paciente_paciente_id_seq', 27, true);
          public          postgres    false    202            @           0    0    reporte_reporte_id_seq    SEQUENCE SET     E   SELECT pg_catalog.setval('public.reporte_reporte_id_seq', 40, true);
          public          postgres    false    204            �
           2606    16954 "   inventario inventario_articulo_key 
   CONSTRAINT     a   ALTER TABLE ONLY public.inventario
    ADD CONSTRAINT inventario_articulo_key UNIQUE (articulo);
 L   ALTER TABLE ONLY public.inventario DROP CONSTRAINT inventario_articulo_key;
       public            postgres    false    208            �
           2606    16952    inventario inventario_pkey 
   CONSTRAINT     c   ALTER TABLE ONLY public.inventario
    ADD CONSTRAINT inventario_pkey PRIMARY KEY (inventario_id);
 D   ALTER TABLE ONLY public.inventario DROP CONSTRAINT inventario_pkey;
       public            postgres    false    208            �
           2606    16880    paciente paciente_pkey 
   CONSTRAINT     ]   ALTER TABLE ONLY public.paciente
    ADD CONSTRAINT paciente_pkey PRIMARY KEY (paciente_id);
 @   ALTER TABLE ONLY public.paciente DROP CONSTRAINT paciente_pkey;
       public            postgres    false    203            �
           2606    16968    paciente paciente_unique 
   CONSTRAINT     i   ALTER TABLE ONLY public.paciente
    ADD CONSTRAINT paciente_unique UNIQUE (nombre, apellido, telefono);
 B   ALTER TABLE ONLY public.paciente DROP CONSTRAINT paciente_unique;
       public            postgres    false    203    203    203            �
           2606    16926    reporte reporte_pkey 
   CONSTRAINT     Z   ALTER TABLE ONLY public.reporte
    ADD CONSTRAINT reporte_pkey PRIMARY KEY (reporte_id);
 >   ALTER TABLE ONLY public.reporte DROP CONSTRAINT reporte_pkey;
       public            postgres    false    205            �
           2606    16930 $   historial historial_paciente_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.historial
    ADD CONSTRAINT historial_paciente_id_fkey FOREIGN KEY (paciente_id) REFERENCES public.paciente(paciente_id) ON UPDATE CASCADE ON DELETE SET NULL;
 N   ALTER TABLE ONLY public.historial DROP CONSTRAINT historial_paciente_id_fkey;
       public          postgres    false    203    2722    206            �
           2606    16935 #   historial historial_reporte_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.historial
    ADD CONSTRAINT historial_reporte_id_fkey FOREIGN KEY (reporte_id) REFERENCES public.reporte(reporte_id) ON UPDATE CASCADE ON DELETE SET NULL;
 M   ALTER TABLE ONLY public.historial DROP CONSTRAINT historial_reporte_id_fkey;
       public          postgres    false    2726    206    205            2   m   x��� ��0�I(�t�9��a!�A�P;4g�DϜ�ߙ;9ׄ���!�mtd!3�ϣ���4���E�se��-��;��V��Ȏ
��%�C�4�N�����;      4   J   x�3�t��O+JM�J�45�2�I,HUpJ�KI,	s�%&� ��9M,��8]R�3��R�K�JR�jb���� =�      /   �  x�eR�n�0|^����؉����(Twp'/���b�ؕ������16I[Z�r�X��Ϻ�k<� {<Z��T�P�v���U	x���݀��+�\��b
~��E)�p��jմ��Jh��>�����o)f���F�����81!���1"l���eQ
Z3^)�P�'�m��0Lt��?�C����8m9�Y9u]M������$�oB�}���[�LLhx�la?�A��A�y,��7ۯ�w���>cʰ��?���(ZzI`-�2�3G&%}Ek��ҡlHoD!(�n5�����9�LV���ެkt��>���� ?��N/X�
�����1�r�^���z~�e�&U�x"$��Yl�y�<����]�M�7��ė�^D�{L�`�����ZwT�ϛl�l����3|���[���b\N�?ﬗ�)O7uժF@
#�M�p19���lܿ��it�q�3F��}��Ӣ�I      1   �  x���[o�@��=�bP�A��1�	��i��H�"^6f+�.Y��˯ﺦ�PC�%��7�s�HN"�x��x}�<!UH%�ޑCG{낸"�T+�^�smV����>~A+ga|���8�'wb������(�L��'�o�3E��ﻝvx��Z�x������I�5L��5��K�/�\z�W�=��n ����_�f�d\�=��TXP2᥻�k��#��^Zbʉ���ótK�>A�G�y���<@tA��6Tl��E��d�SB\ �� !9"��#A�/B)��Cs[�/5����M��	�&�Z�?�u[9���o��6k�����|�_o?�@vY��z�<ȄK�Ѯ�T�ǖ� )�畱~v����n�i��H}$���-��#��?M`km(�X��F�x�C�d�k�5���,nT�$��I��XՎ ������u���=ks���G� �k�c�     