PGDMP      0            	    {            netflix    16.0    16.0                0    0    ENCODING    ENCODING        SET client_encoding = 'UTF8';
                      false                       0    0 
   STDSTRINGS 
   STDSTRINGS     (   SET standard_conforming_strings = 'on';
                      false                       0    0 
   SEARCHPATH 
   SEARCHPATH     8   SELECT pg_catalog.set_config('search_path', '', false);
                      false                       1262    16398    netflix    DATABASE     i   CREATE DATABASE netflix WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE_PROVIDER = libc LOCALE = 'C';
    DROP DATABASE netflix;
                postgres    false            �            1259    16671    actors    TABLE     �   CREATE TABLE public.actors (
    name character varying(125),
    surname character varying(125),
    year_of_birth integer,
    gender character varying(50),
    show_id integer
);
    DROP TABLE public.actors;
       public         heap    postgres    false            �            1259    16665    shows    TABLE       CREATE TABLE public.shows (
    show_id integer NOT NULL,
    title character varying(125),
    genre character varying(125),
    release_year integer,
    imdb_grade double precision,
    creator character varying(125),
    number_of_episodes integer,
    number_of_seasons integer
);
    DROP TABLE public.shows;
       public         heap    postgres    false            �            1259    16664    shows_show_id_seq    SEQUENCE     �   CREATE SEQUENCE public.shows_show_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 (   DROP SEQUENCE public.shows_show_id_seq;
       public          postgres    false    216                       0    0    shows_show_id_seq    SEQUENCE OWNED BY     G   ALTER SEQUENCE public.shows_show_id_seq OWNED BY public.shows.show_id;
          public          postgres    false    215            w           2604    16668    shows show_id    DEFAULT     n   ALTER TABLE ONLY public.shows ALTER COLUMN show_id SET DEFAULT nextval('public.shows_show_id_seq'::regclass);
 <   ALTER TABLE public.shows ALTER COLUMN show_id DROP DEFAULT;
       public          postgres    false    216    215    216                      0    16671    actors 
   TABLE DATA           O   COPY public.actors (name, surname, year_of_birth, gender, show_id) FROM stdin;
    public          postgres    false    217   �                 0    16665    shows 
   TABLE DATA           �   COPY public.shows (show_id, title, genre, release_year, imdb_grade, creator, number_of_episodes, number_of_seasons) FROM stdin;
    public          postgres    false    216   |                  0    0    shows_show_id_seq    SEQUENCE SET     @   SELECT pg_catalog.setval('public.shows_show_id_seq', 11, true);
          public          postgres    false    215            y           2606    16670    shows shows_pkey 
   CONSTRAINT     S   ALTER TABLE ONLY public.shows
    ADD CONSTRAINT shows_pkey PRIMARY KEY (show_id);
 :   ALTER TABLE ONLY public.shows DROP CONSTRAINT shows_pkey;
       public            postgres    false    216            z           2606    16674    actors actors_show_id_fkey    FK CONSTRAINT     ~   ALTER TABLE ONLY public.actors
    ADD CONSTRAINT actors_show_id_fkey FOREIGN KEY (show_id) REFERENCES public.shows(show_id);
 D   ALTER TABLE ONLY public.actors DROP CONSTRAINT actors_show_id_fkey;
       public          postgres    false    216    217    3449               w  x�M��n�0�ϻ��*B�cJ�)��
R/�,`�%c#�AJ��6�Q�;�ff�K]+��`n����S���.��P'$%��I�a�J�����4+`6��oBJضR^�#+���߅�ݍ��;�E�X�c�%�=��8��|q���1$ �1�V4!'gᄌ$������"6�W��}���)2.[8��5�ڷ��AJqK��R��i���?s����E�S(�P�X�;�6�{��i��W���mC�Q�ᖟRJ���4�̒�� 3��*�����ay_%�]-��kit�qsuQ��_�g�w�R\e$��>,�4�{��<�v��^	��},T��2�+��Ú���)�ї�6�����b�v{��"�d���         v  x�UQ�n�0>SO�'*+�;��`k�`)腈Y[�-��o?ڇ�I��_j8Z���E��Ȑ=��M?=�]O� ��Le��3��s�.75�9�Mf�w�&��2p�ib�_�LA^��FZ F�Kh�^�0, (j�*H�X�-ȃ�q��|X����ho�?rԑ�Z�pb�������p�HV��ǆb���"Y���v�"�xN�n�"��F+�XH��t�-����B؎�0���w<ね�=0K��Ɠu[����凧̬�'J����3T����G���2�~|a:�_4�(%���.6^{YȮ���)�qkaz%�8<_�ѶQ���`�=d�֠�f�����Ϗ픫Z,9����3lk���F)�d�     