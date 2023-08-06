import pytest
from django.core.management import call_command


class TestImportCommand:
    @pytest.mark.command
    def test_objects_creation(self, import_translations_fixture):
        """Check importing of translations."""
        from translate.service.models import Language, Translation, TranslationKey

        language = Language.objects.get(lang_info="de")
        translation_record = Translation.objects.filter(translation="Startdatum auf Webseite").first()
        key_record = TranslationKey.objects.get(snake_name="admin_landlord_request")

        assert language
        assert language.lang_info == "de"
        assert translation_record
        assert translation_record.key
        assert translation_record.language.lang_info == "de"
        assert key_record
        assert key_record.snake_name
        assert key_record.id_name
        assert key_record.Category

    @pytest.mark.command
    def test_command_idempotency(self, import_translations_fixture):
        """
        Test the re-execution of the command
        """
        from translate.service.models import Language, Translation, TranslationKey

        languages = Language.objects.all()
        translations = Translation.objects.all()
        keys = TranslationKey.objects.all()

        assert len(languages) == 1
        assert len(translations) == 8
        assert len(keys) == 9

        for key in keys:
            assert key.usage_context is None, "All imported keys should not have context"
            TranslationKey.objects.filter(id=key.id).update(usage_context="Add some new context")
            key.refresh_from_db()

        # recall the command to test if it will overwrite usage_context
        call_command("import_translations", translations_dir="translate/service/tests/fixtures")

        reloaded_keys = TranslationKey.objects.all()
        for key in reloaded_keys:
            assert key.usage_context == "Add some new context", "Context should not be overwritten by same import"

        # recall of the command should not insert any new keys
        assert len(languages) == 1
        assert len(translations) == 8, "Translations number should stay the same"
        assert len(keys) == 9, "Keys number should stayed the same"

        # cleanup
        Translation.objects.all().delete()
        TranslationKey.objects.all().delete()
        Language.objects.all().delete()


class TestKeysNoContextDeletion:
    @pytest.mark.command
    def test_objects_deletion(self, import_translations_fixture):
        """Check deletion of translation keys with no usage_context."""
        from translate.service.models import Translation, TranslationKey

        record = Translation.objects.all()
        key_record = TranslationKey.objects.all()

        assert len(record) == 8
        assert len(key_record) == 9

        for key in key_record:
            assert key.usage_context is None

        call_command("delete_no_context_keys")

        new_list_keys = list(TranslationKey.objects.all())

        assert len(new_list_keys) == 0, "Since no imported keys have usage_context, they should all be deleted"

    @pytest.mark.command
    def test_skipping_keys_with_context(self, import_translations_fixture):
        """Test not deleting key with usage_context"""
        from translate.service.models import Translation, TranslationKey

        record = Translation.objects.all()
        key_record = TranslationKey.objects.all()

        assert len(record) == 8
        assert len(key_record) == 9

        # Add usage context for every imported key
        for key in key_record:
            TranslationKey.objects.filter(id=key.id).update(usage_context="Add some new context")
            key.refresh_from_db()

        # call the command
        call_command("delete_no_context_keys")

        assert len(record) == 8, "Translation count should stay same after calling of command"
        assert len(key_record) == 9, "TranslationKeys count should stay same after calling of command"
