from fastapi import HTTPException

from main import RecipeIn, create_recipe, get_recipe, list_recipes, shopping_list


def test_create_and_get_recipe():
    recipe = create_recipe(
        RecipeIn(title="Pancakes", ingredients=["flour", "milk"], tags=["breakfast"])
    )
    assert get_recipe(recipe["id"])["title"] == "Pancakes"
    assert get_recipe(recipe["id"])["tags"] == ["breakfast"]


def test_list_recipes():
    create_recipe(RecipeIn(title="Toast"))
    assert any(rec["title"] == "Toast" for rec in list_recipes())


def test_unknown_recipe_404():
    try:
        get_recipe(99999)
    except HTTPException as exc:
        assert exc.status_code == 404
    else:
        raise AssertionError("missing recipe should raise HTTPException")


def test_shopping_list_deduplicates_in_first_seen_order():
    first = create_recipe(
        RecipeIn(title="Soup", ingredients=["onion", "carrot", "salt"])
    )["id"]
    second = create_recipe(
        RecipeIn(title="Stew", ingredients=["carrot", "potato", "salt"])
    )["id"]
    assert shopping_list(f"{first},{second}") == ["onion", "carrot", "salt", "potato"]
