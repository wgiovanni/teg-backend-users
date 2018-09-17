-- Table: public.role

-- DROP TABLE public.role;

CREATE TABLE public.role
(
  id integer NOT NULL DEFAULT nextval('role_id_seq'::regclass),
  name character varying(50) NOT NULL,
  CONSTRAINT id_role PRIMARY KEY (id)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE public.role
  OWNER TO postgres;
