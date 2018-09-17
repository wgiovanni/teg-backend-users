-- Table: public."user"

-- DROP TABLE public."user";

CREATE TABLE public."user"
(
  id integer NOT NULL DEFAULT nextval('user_id_seq'::regclass),
  first_name character varying(50) NOT NULL,
  last_name character varying(50) NOT NULL,
  email character varying(100) NOT NULL,
  password character varying(100) NOT NULL,
  id_role integer NOT NULL,
  CONSTRAINT user_pkey PRIMARY KEY (id),
  CONSTRAINT id_role FOREIGN KEY (id_role)
      REFERENCES public.role (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION
)
WITH (
  OIDS=FALSE
);
ALTER TABLE public."user"
  OWNER TO postgres;

-- Index: public.fki_id_role

-- DROP INDEX public.fki_id_role;

CREATE INDEX fki_id_role
  ON public."user"
  USING btree
  (id_role);

