SELECT
    TotalPerson.prod_unid AS  Produto,
    TotalPerson.empresa_unid AS  Empresa,
    TotalPerson.NomeFantasia_emp  AS NomeFantasia,
    TotalPerson.obra_unid AS  Obra,
    UPPER(TotalPerson.identificador_unid) AS Unidade,
    CASE
                        WHEN UPPER(TotalPerson.identificador_unid) LIKE 'A%' THEN 'ALMOXERIFADO'
                        WHEN UPPER(TotalPerson.identificador_unid) LIKE 'E%' THEN 'ESCANINHOS'
                        WHEN UPPER(TotalPerson.identificador_unid) LIKE 'L%' THEN 'LOJAS'
                        WHEN UPPER(TotalPerson.identificador_unid) LIKE 'V%' THEN 'VAGA VEICULOS'
                        WHEN UPPER(TotalPerson.identificador_unid) LIKE 'G%' THEN 'VAGA VEICULOS'
                        WHEN UPPER(TotalPerson.identificador_unid) LIKE 'M%' THEN 'VAGA MOTOS'
                        WHEN UPPER(TotalPerson.identificador_unid) LIKE '%MT' THEN 'VAGA MOTOS'
                        WHEN TotalPerson.empresa_unid IN (76) THEN 'SALA COMERCIAL'
                        WHEN TotalPerson.empresa_unid IN (58,75,96,98,106) THEN 'LOTE RESIDENCIAL'
                    ELSE 'APARTAMENTO RESIDENCIAL' END  AS  Tipo,
    TotalPerson.codtipprod_unid AS Cod_Tipologia,
    TotalPerson.descricao_tipprod AS  Tipologia,
    UPPER(TotalPerson.Descr_status) AS Status
FROM (
                SELECT
        UP.prod_unid,
        UP.empresa_unid,
        CASE
                        WHEN UP.empresa_unid = 42 AND UP.obra_unid LIKE '2T%' THEN 'CITY PARK PALACE'
                        WHEN UP.empresa_unid = 42 AND UP.obra_unid LIKE '3T%' THEN 'CITY PARK ROYAL'
                        WHEN UP.empresa_unid = 42 AND UP.obra_unid LIKE '420%' THEN 'CITY PARK MAJESTIC'
                    ELSE E.NomeFantasia_emp END AS NomeFantasia_emp,
        UP.obra_unid,
        --O.descr_obr,
        UP.identificador_unid,
        UP.codtipprod_unid,
        TP.descricao_tipprod,
        CASE
                        WHEN UP.vendido_unid = 0 THEN 'Disponível'
                        WHEN UP.vendido_unid = 1 THEN
                            (CASE WHEN UD.tipocontrato_udt IN( 1, 2, 5 ) THEN 'Locada' ELSE 'Vendida' END)
                        WHEN UP.vendido_unid = 2 THEN 'Reservado'
                        WHEN UP.vendido_unid = 3 THEN 'Proposta'
                        WHEN UP.vendido_unid = 4 THEN 'Quitado'
                        WHEN UP.vendido_unid = 5 THEN 'Escriturado'
                        WHEN UP.vendido_unid = 6 THEN 'Em venda'
                        WHEN UP.vendido_unid = 7 THEN 'Suspenso'
                        WHEN UP.vendido_unid = 8 THEN 'Fora de venda'
                        WHEN UP.vendido_unid = 9 THEN 'Em acerto'
                        WHEN UP.vendido_unid = 10 THEN 'Dação' END AS Descr_status
    FROM UAU.dbo.UnidadePer AS UP

        LEFT JOIN UAU.dbo.UnidadeDetalhe AS UD
        ON UP.empresa_unid = UD.empresa_udt
            AND UP.prod_unid = UD.prod_udt
            AND UP.numper_unid = UD.numper_udt

        LEFT JOIN UAU.dbo.tipologiaproducao AS TP
        ON TP.codigo_tipprod = UP.codtipprod_unid

        LEFT JOIN UAU.dbo.Empresas AS E
        ON UP.empresa_unid = E.Codigo_emp

        LEFT JOIN UAU.dbo.Obras AS O
        ON UP.obra_unid = O.cod_obr
            AND UP.empresa_unid = O.Empresa_obr
            
            
            )  AS TotalPerson

WHERE TotalPerson.prod_unid NOT IN (36,58,65)
    AND TotalPerson.empresa_unid NOT IN (9,19,78)
    AND (TotalPerson.identificador_unid IS NOT NULL
    AND TotalPerson.identificador_unid NOT LIKE '')
    AND TotalPerson.Descr_status = 'DISPONÍVEL'
    AND TotalPerson.obra_unid LIKE '%I'