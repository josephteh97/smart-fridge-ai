"""
AI-Powered Recipe Generator
Generates recipes using expiring ingredients
"""
from typing import List, Dict, Optional
import json
from loguru import logger
import config


class RecipeGenerator:
    """Generates recipes from available ingredients using AI"""
    
    def __init__(self):
        self.api_key = config.RECIPE_API_KEY
    
    def generate_recipe(self, ingredients: List[str], 
                       cuisine_type: str = None,
                       dietary_restrictions: List[str] = None) -> Dict:
        """Generate a recipe using AI based on available ingredients"""
        
        # Format ingredients list
        ingredients_text = ", ".join(ingredients)
        
        # Build prompt
        prompt = f"""Create a delicious recipe using the following ingredients that are about to expire:
{ingredients_text}

Requirements:
- Use as many of these ingredients as possible
- The recipe should be practical and easy to prepare
- Include preparation time and cooking time
- Provide step-by-step instructions"""
        
        if cuisine_type:
            prompt += f"\n- Cuisine type: {cuisine_type}"
        
        if dietary_restrictions:
            restrictions_text = ", ".join(dietary_restrictions)
            prompt += f"\n- Dietary restrictions: {restrictions_text}"
        
        prompt += "\n\nProvide the recipe in the following JSON format:\n"
        prompt += """{
    "name": "Recipe Name",
    "description": "Brief description",
    "cuisine_type": "Cuisine",
    "prep_time": 15,
    "cook_time": 30,
    "servings": 4,
    "ingredients": [
        {"item": "ingredient 1", "amount": "quantity", "unit": "measurement"},
        {"item": "ingredient 2", "amount": "quantity", "unit": "measurement"}
    ],
    "instructions": [
        "Step 1: Do this",
        "Step 2: Do that"
    ],
    "tips": ["Optional cooking tips"]
}"""
        
        try:
            # Try using OpenAI API if available
            if self.api_key:
                recipe = self._generate_with_openai(prompt)
            else:
                # Fallback to rule-based recipe generation
                recipe = self._generate_fallback_recipe(ingredients)
            
            logger.info(f"Generated recipe: {recipe.get('name', 'Unknown')}")
            return recipe
            
        except Exception as e:
            logger.error(f"Recipe generation failed: {e}")
            return self._generate_fallback_recipe(ingredients)
    
    def _generate_with_openai(self, prompt: str) -> Dict:
        """Generate recipe using OpenAI API"""
        try:
            import openai
            
            openai.api_key = self.api_key
            
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a professional chef and recipe creator. Generate creative and practical recipes."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=1000
            )
            
            recipe_text = response.choices[0].message.content
            
            # Parse JSON from response
            recipe_json = self._extract_json_from_text(recipe_text)
            
            return recipe_json
            
        except Exception as e:
            logger.error(f"OpenAI API error: {e}")
            raise
    
    def _extract_json_from_text(self, text: str) -> Dict:
        """Extract JSON from text response"""
        try:
            # Try to find JSON in the text
            start_idx = text.find('{')
            end_idx = text.rfind('}') + 1
            
            if start_idx != -1 and end_idx > start_idx:
                json_str = text[start_idx:end_idx]
                return json.loads(json_str)
            else:
                raise ValueError("No JSON found in response")
                
        except Exception as e:
            logger.error(f"JSON extraction failed: {e}")
            raise
    
    def _generate_fallback_recipe(self, ingredients: List[str]) -> Dict:
        """Generate a simple fallback recipe"""
        # Simple rule-based recipe generation
        recipe_templates = [
            {
                'name': 'Quick Stir Fry',
                'description': 'A quick and healthy stir fry using available ingredients',
                'cuisine_type': 'Asian Fusion',
                'prep_time': 10,
                'cook_time': 15,
                'servings': 2,
                'instructions': [
                    'Heat oil in a large wok or skillet over high heat',
                    'Add vegetables and stir fry for 3-4 minutes',
                    'Add protein (if available) and cook until done',
                    'Season with soy sauce, garlic, and ginger',
                    'Serve hot over rice or noodles'
                ],
                'tips': ['Use high heat for best results', 'Don\'t overcrowd the pan']
            },
            {
                'name': 'Fresh Salad Bowl',
                'description': 'Healthy and refreshing salad using fresh ingredients',
                'cuisine_type': 'Mediterranean',
                'prep_time': 15,
                'cook_time': 0,
                'servings': 2,
                'instructions': [
                    'Wash and chop all fresh vegetables',
                    'Combine in a large bowl',
                    'Add protein of choice (if available)',
                    'Dress with olive oil, lemon juice, and herbs',
                    'Season with salt and pepper to taste'
                ],
                'tips': ['Use fresh, crisp vegetables', 'Dress just before serving']
            },
            {
                'name': 'One-Pot Wonder',
                'description': 'Easy one-pot meal using available ingredients',
                'cuisine_type': 'Home Cooking',
                'prep_time': 10,
                'cook_time': 25,
                'servings': 4,
                'instructions': [
                    'Heat oil in a large pot',
                    'Sauté aromatics (onions, garlic) until fragrant',
                    'Add vegetables and protein',
                    'Add liquid (broth or water) and bring to boil',
                    'Simmer until everything is cooked through',
                    'Season to taste and serve'
                ],
                'tips': ['Layer ingredients by cooking time', 'Don\'t rush the process']
            }
        ]
        
        # Select template based on ingredients
        selected_template = recipe_templates[0]  # Default to stir fry
        
        # Categorize ingredients
        has_vegetables = any('vegetable' in str(ing).lower() or 
                           any(veg in str(ing).lower() for veg in 
                           ['carrot', 'broccoli', 'lettuce', 'tomato', 'cucumber'])
                           for ing in ingredients)
        
        has_protein = any(prot in str(ing).lower() for prot in 
                         ['chicken', 'beef', 'pork', 'fish', 'tofu', 'eggs']
                         for ing in ingredients)
        
        if not has_protein and has_vegetables:
            selected_template = recipe_templates[1]  # Salad
        elif len(ingredients) >= 4:
            selected_template = recipe_templates[2]  # One-pot
        
        # Build ingredient list
        ingredient_list = []
        for ing in ingredients:
            ingredient_list.append({
                'item': ing,
                'amount': '1',
                'unit': 'portion'
            })
        
        recipe = selected_template.copy()
        recipe['ingredients'] = ingredient_list
        recipe['used_ingredients'] = ingredients
        
        return recipe
    
    def save_recipe_to_file(self, recipe: Dict, filename: str = None) -> str:
        """Save recipe to a file"""
        import os
        from datetime import datetime
        
        if filename is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"recipe_{timestamp}.json"
        
        save_dir = os.path.join(config.BASE_DIR, 'data', 'recipes')
        os.makedirs(save_dir, exist_ok=True)
        
        filepath = os.path.join(save_dir, filename)
        
        with open(filepath, 'w') as f:
            json.dump(recipe, f, indent=2)
        
        logger.info(f"Recipe saved to {filepath}")
        return filepath
    
    def format_recipe_for_display(self, recipe: Dict) -> str:
        """Format recipe as readable text"""
        output = f"🍽️ {recipe['name']}\n"
        output += "=" * 50 + "\n\n"
        
        output += f"📝 Description: {recipe.get('description', 'N/A')}\n"
        output += f"🌍 Cuisine: {recipe.get('cuisine_type', 'N/A')}\n"
        output += f"⏱️ Prep Time: {recipe.get('prep_time', 'N/A')} mins\n"
        output += f"🔥 Cook Time: {recipe.get('cook_time', 'N/A')} mins\n"
        output += f"👥 Servings: {recipe.get('servings', 'N/A')}\n\n"
        
        output += "📦 INGREDIENTS:\n"
        output += "-" * 50 + "\n"
        for ing in recipe.get('ingredients', []):
            if isinstance(ing, dict):
                output += f"• {ing.get('amount', '')} {ing.get('unit', '')} {ing.get('item', '')}\n"
            else:
                output += f"• {ing}\n"
        
        output += "\n📋 INSTRUCTIONS:\n"
        output += "-" * 50 + "\n"
        for i, step in enumerate(recipe.get('instructions', []), 1):
            output += f"{i}. {step}\n"
        
        if recipe.get('tips'):
            output += "\n💡 TIPS:\n"
            output += "-" * 50 + "\n"
            for tip in recipe['tips']:
                output += f"• {tip}\n"
        
        return output
    
    def generate_shopping_list(self, recipe: Dict, available_ingredients: List[str]) -> List[str]:
        """Generate shopping list for missing ingredients"""
        required_ingredients = [ing['item'] if isinstance(ing, dict) else ing 
                              for ing in recipe.get('ingredients', [])]
        
        available_lower = [ing.lower() for ing in available_ingredients]
        
        shopping_list = []
        for ingredient in required_ingredients:
            if ingredient.lower() not in available_lower:
                shopping_list.append(ingredient)
        
        return shopping_list
