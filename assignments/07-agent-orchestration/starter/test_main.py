from main import RecipeIn, create_recipe, get_recipe, list_recipes, scaled_recipe


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
    from fastapi import HTTPException

    try:
        get_recipe(99999)
    except HTTPException as exc:
        assert exc.status_code == 404
    else:
        raise AssertionError("missing recipe should raise HTTPException")


def test_scaled_recipe_doubles_numeric_ingredients():
    recipe = create_recipe(
        RecipeIn(title="Pancakes", ingredients=["200 g flour", "2 eggs", "salt"])
    )
    result = scaled_recipe(recipe["id"], factor=2)
    assert result["ingredients"] == ["400 g flour", "4 eggs", "salt"]
