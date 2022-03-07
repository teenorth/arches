# Generated by Django 2.2.24 on 2021-12-03 13:27

import re
import uuid
import django.contrib.postgres.fields.jsonb
import django.core.validators
from django.db import migrations, models
from arches.app.models.system_settings import settings

add_etl_manager = """
    insert into plugins (
        pluginid,
        name,
        icon,
        component,
        componentname,
        config,
        slug,
        sortorder)
    values (
        '7720e9fa-876c-4127-a77a-b099cd2a5d45',
        'ETL Manager',
        'fa fa-database',
        'views/components/plugins/etl-manager',
        'etl-manager',
        '{"show": true}',
        'etl-manager',
        2);
    """
remove_etl_manager = """
    delete from plugins where pluginid = '7720e9fa-876c-4127-a77a-b099cd2a5d45';
    """

add_csv_importer = """
    insert into etl_modules (
        etlmoduleid,
        name,
        description,
        component,
        componentname,
        modulename,
        classname,
        config,
        icon,
        slug)
    values (
        '0a0cea7e-b59a-431a-93d8-e9f8c41bdd6b',
        'Import Single CSV',
        'Import a Single CSV file to Arches',
        'views/components/etl_modules/import-single-csv',
        'import-single-csv',
        'import_single_csv.py',
        'ImportSingleCsv',
        '{"bgColor": "#9591ef", "circleColor": "#b0adf3"}',
        'fa fa-upload',
        'import-single-csv');
    """
remove_csv_importer = """
    delete from etl_modules where etlmoduleid = '0a0cea7e-b59a-431a-93d8-e9f8c41bdd6b';
    """

add_validation_reporting_functions = """
    CREATE OR REPLACE FUNCTION public.__arches_get_error_messages(json_obj jsonb)
    RETURNS text
    LANGUAGE plpgsql AS

    $func$
    DECLARE
        _key   text;
        _value jsonb;
        _result text;
        _note text;

    BEGIN
        FOR _key, _value IN 
            SELECT * FROM jsonb_each_text($1)
        LOOP
            IF _value ->> 'valid' = 'false' THEN
                IF _value ->> 'notes' IS NULL THEN
                    _note = 'unspecified error';
                END IF; 
                -- we could add the nodeid (_key), but let's not be verbose just yet
                IF _result IS NULL THEN
                _result := _note;
                ELSE
                _result := '|' || _node;
                END IF;
            END IF;
        END LOOP;
        RETURN _result;
    END;
    $func$;

    CREATE OR REPLACE FUNCTION public.__arches_collect_node_validation(transaction_id uuid)
    RETURNS TABLE(source text, message text, transactionid uuid)
    AS $$
    SELECT source_description, __arches_get_error_messages(value) AS message, transactionid
    FROM load_staging 
    WHERE passes_validation IS NOT true
    AND transactionid = transaction_id;  
    $$
    LANGUAGE SQL;
    """

remove_validation_reporting_functions = """
    DROP FUNCTION public.__arches_get_error_messages(json_obj jsonb);
    DROP FUNCTION public.__arches_collect_node_validation(transaction_id uuid);
    """

class Migration(migrations.Migration):

    dependencies = [
        ("models", "7874_node_alias"),
    ]

    operations = [
        migrations.CreateModel(
            name="ETLModule",
            fields=[
                ("etlmoduleid", models.UUIDField(default=uuid.uuid1, primary_key=True, serialize=False)),
                ("name", models.TextField()),
                ("description", models.TextField(blank=True, null=True)),
                ("component", models.TextField()),
                ("componentname", models.TextField()),
                ("modulename", models.TextField(blank=True, null=True)),
                ("classname", models.TextField(blank=True, null=True)),
                ("config", django.contrib.postgres.fields.jsonb.JSONField(blank=True, db_column="config", null=True)),
                ("icon", models.TextField()),
                (
                    "slug",
                    models.TextField(
                        null=True,
                        unique=True,
                        validators=[
                            django.core.validators.RegexValidator(
                                re.compile("^[-a-zA-Z0-9_]+\\Z"),
                                "Enter a valid 'slug' consisting of letters, numbers, underscores or hyphens.",
                                "invalid",
                            )
                        ],
                    ),
                ),
            ],
            options={
                "db_table": "etl_modules",
                "managed": True,
            },
        ),
        migrations.RunSQL(
            add_etl_manager,
            remove_etl_manager,
        ),
        migrations.RunSQL(
            add_csv_importer,
            remove_csv_importer,
        ),
        migrations.CreateModel(
            name="LoadEvent",
            fields=[
                ("transactionid", models.UUIDField(default=uuid.uuid1, primary_key=True, serialize=False)),
                ("complete", models.BooleanField(default=False)),
                ("succssful", models.BooleanField(blank=True, null=True)),
                ("load_description", models.TextField(blank=True, null=True)),
                ("message", models.TextField(blank=True, null=True)),
                ("load_start_time", models.DateTimeField(blank=True, null=True)),
                ("load_end_time", models.DateTimeField(blank=True, null=True)),
                ("user", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                "db_table": "load_event",
                "managed": True,
            },
        ),
        migrations.CreateModel(
            name="LoadStaging",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("value", django.contrib.postgres.fields.jsonb.JSONField(blank=True, db_column="value", null=True)),
                ("legacyid", models.TextField(blank=True, null=True)),
                ("resourceid", models.UUIDField(blank=True, null=True, serialize=False)),
                ("tileid", models.UUIDField(blank=True, null=True, serialize=False)),
                ("parenttileid", models.UUIDField(blank=True, null=True, serialize=False)),
                ("passes_validation", models.BooleanField(blank=True, null=True)),
                ("nodegroup_depth", models.IntegerField(default=1)),
                ("source_description", models.TextField(blank=True, null=True)),
                ("message", models.TextField(blank=True, null=True)),
                (
                    "load_event",
                    models.ForeignKey(db_column="transactionid", on_delete=django.db.models.deletion.CASCADE, to="models.LoadEvent"),
                ),
                (
                    "nodegroup",
                    models.ForeignKey(db_column="nodegroupid", on_delete=django.db.models.deletion.CASCADE, to="models.NodeGroup"),
                ),
            ],
            options={
                "db_table": "load_staging",
                "managed": True,
            },
        ),
        migrations.RunSQL(
            add_validation_reporting_functions,
            remove_validation_reporting_functions
        ),
    ]
