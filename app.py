from flask import Flask, render_template, request, send_file
import os
from waitress import serve

app = Flask(__name__)

# Full list of valid materials from the Spigot API
MATERIALS = [
    'ACACIA_BOAT', 'ACACIA_BUTTON', 'ACACIA_CHEST_BOAT', 'ACACIA_DOOR', 'ACACIA_FENCE', 'ACACIA_FENCE_GATE',
    'ACACIA_HANGING_SIGN', 'ACACIA_LEAVES', 'ACACIA_LOG', 'ACACIA_PLANKS', 'ACACIA_PRESSURE_PLATE',
    'ACACIA_SAPLING', 'ACACIA_SIGN', 'ACACIA_SLAB', 'ACACIA_STAIRS', 'ACACIA_TRAPDOOR', 'ACACIA_WOOD',
    'ACTIVATOR_RAIL', 'AIR', 'ALLIUM', 'AMETHYST_BLOCK', 'AMETHYST_CLUSTER', 'ANCIENT_DEBRIS', 'ANDESITE',
    'ANDESITE_SLAB', 'ANDESITE_STAIRS', 'ANDESITE_WALL', 'ANVIL', 'APPLE', 'ARMOR_STAND', 'ARROW', 'AXOLOTL_BUCKET',
    'AZALEA', 'AZALEA_LEAVES', 'AZURE_BLUET', 'BAMBOO', 'BAMBOO_BLOCK', 'BAMBOO_BUTTON', 'BAMBOO_CHEST_RAFT',
    'BAMBOO_DOOR', 'BAMBOO_FENCE', 'BAMBOO_FENCE_GATE', 'BAMBOO_HANGING_SIGN', 'BAMBOO_MOSAIC', 'BAMBOO_MOSAIC_SLAB',
    'BAMBOO_MOSAIC_STAIRS', 'BAMBOO_PLANKS', 'BAMBOO_PRESSURE_PLATE', 'BAMBOO_RAFT', 'BAMBOO_SAPLING', 'BAMBOO_SIGN',
    'BAMBOO_SLAB', 'BAMBOO_STAIRS', 'BAMBOO_TRAPDOOR', 'BARREL', 'BARRIER', 'BASALT', 'BAT_SPAWN_EGG', 'BEACON',
    'BEDROCK', 'BEE_NEST', 'BEE_SPAWN_EGG', 'BEEF', 'BEEHIVE', 'BEETROOT', 'BEETROOT_SEEDS', 'BEETROOT_SOUP', 'BELL',
    'BIG_DRIPLEAF', 'BIRCH_BOAT', 'BIRCH_BUTTON', 'BIRCH_CHEST_BOAT', 'BIRCH_DOOR', 'BIRCH_FENCE', 'BIRCH_FENCE_GATE',
    'BIRCH_HANGING_SIGN', 'BIRCH_LEAVES', 'BIRCH_LOG', 'BIRCH_PLANKS', 'BIRCH_PRESSURE_PLATE', 'BIRCH_SAPLING',
    'BIRCH_SIGN', 'BIRCH_SLAB', 'BIRCH_STAIRS', 'BIRCH_TRAPDOOR', 'BIRCH_WOOD', 'BLACK_BANNER', 'BLACK_BED',
    'BLACK_CANDLE', 'BLACK_CARPET', 'BLACK_CONCRETE', 'BLACK_CONCRETE_POWDER', 'BLACK_DYE', 'BLACK_GLAZED_TERRACOTTA',
    'BLACK_SHULKER_BOX', 'BLACK_STAINED_GLASS', 'BLACK_STAINED_GLASS_PANE', 'BLACK_TERRACOTTA', 'BLACK_WOOL',
    'BLACKSTONE', 'BLACKSTONE_SLAB', 'BLACKSTONE_STAIRS', 'BLACKSTONE_WALL', 'BLAST_FURNACE', 'BLAZE_POWDER',
    'BLAZE_ROD', 'BLAZE_SPAWN_EGG', 'BLUE_BANNER', 'BLUE_BED', 'BLUE_CANDLE', 'BLUE_CARPET', 'BLUE_CONCRETE',
    'BLUE_CONCRETE_POWDER', 'BLUE_DYE', 'BLUE_GLAZED_TERRACOTTA', 'BLUE_ICE', 'BLUE_ORCHID', 'BLUE_SHULKER_BOX',
    'BLUE_STAINED_GLASS', 'BLUE_STAINED_GLASS_PANE', 'BLUE_TERRACOTTA', 'BLUE_WOOL', 'BONE', 'BONE_BLOCK',
    'BONE_MEAL', 'BOOK', 'BOOKSHELF', 'BOW', 'BOWL', 'BRAIN_CORAL', 'BRAIN_CORAL_BLOCK', 'BRAIN_CORAL_FAN',
    'BRAIN_CORAL_WALL_FAN', 'BREAD', 'BREWING_STAND', 'BRICK', 'BRICK_SLAB', 'BRICK_STAIRS', 'BRICK_WALL',
    'BRICKS', 'BROWN_BANNER', 'BROWN_BED', 'BROWN_CANDLE', 'BROWN_CARPET', 'BROWN_CONCRETE', 'BROWN_CONCRETE_POWDER',
    'BROWN_DYE', 'BROWN_GLAZED_TERRACOTTA', 'BROWN_MUSHROOM', 'BROWN_MUSHROOM_BLOCK', 'BROWN_SHULKER_BOX',
    'BROWN_STAINED_GLASS', 'BROWN_STAINED_GLASS_PANE', 'BROWN_TERRACOTTA', 'BROWN_WOOL', 'BUBBLE_CORAL',
    'BUBBLE_CORAL_BLOCK', 'BUBBLE_CORAL_FAN', 'BUBBLE_CORAL_WALL_FAN', 'BUCKET', 'BUDDING_AMETHYST', 'BUNDLE',
    'BURNING_STICK', 'CACTUS', 'CAKE', 'CALCITE', 'CAMPFIRE', 'CANDLE', 'CARROT', 'CARROT_ON_A_STICK', 'CARROTS',
    'CARTOGRAPHY_TABLE', 'CARVED_PUMPKIN', 'CAT_SPAWN_EGG', 'CAULDRON', 'CAVE_SPIDER_SPAWN_EGG', 'CAVE_VINES',
    'CAVE_VINES_PLANT', 'CHAIN', 'CHAIN_COMMAND_BLOCK', 'CHAINMAIL_BOOTS', 'CHAINMAIL_CHESTPLATE', 'CHAINMAIL_HELMET',
    'CHAINMAIL_LEGGINGS', 'CHARCOAL', 'CHEST', 'CHEST_MINECART', 'CHICKEN', 'CHICKEN_SPAWN_EGG', 'CHISELED_BOOKSHELF',
    'CHISELED_DEEPSLATE', 'CHISELED_NETHER_BRICKS', 'CHISELED_POLISHED_BLACKSTONE', 'CHISELED_QUARTZ_BLOCK',
    'CHISELED_RED_SANDSTONE', 'CHISELED_SANDSTONE', 'CHISELED_STONE_BRICKS', 'CHORUS_FLOWER', 'CHORUS_FRUIT',
    'CHORUS_PLANT', 'CLAY', 'CLAY_BALL', 'CLOCK', 'COAL', 'COAL_BLOCK', 'COAL_ORE', 'COARSE_DIRT', 'COBBLESTONE',
    'COBBLESTONE_SLAB', 'COBBLESTONE_STAIRS', 'COBBLESTONE_WALL', 'COBWEB', 'COCOA_BEANS', 'COD', 'COD_BUCKET',
    'COD_SPAWN_EGG', 'COMMAND_BLOCK', 'COMMAND_BLOCK_MINECART', 'COMPARATOR', 'COMPASS', 'COMPOSTER', 'CONDUIT',
    'COOKED_BEEF', 'COOKED_CHICKEN', 'COOKED_COD', 'COOKED_MUTTON', 'COOKED_PORKCHOP', 'COOKED_RABBIT',
    'COOKED_SALMON', 'COOKIE', 'COPPER_BLOCK', 'COPPER_INGOT', 'COPPER_ORE', 'CORNFLOWER', 'COW_SPAWN_EGG', 'CRACKED_DEEPSLATE_BRICKS',
    'CRACKED_DEEPSLATE_TILES', 'CRACKED_NETHER_BRICKS', 'CRACKED_POLISHED_BLACKSTONE_BRICKS', 'CRACKED_STONE_BRICKS',
    'CRAFTING_TABLE', 'CREEPER_BANNER_PATTERN', 'CREEPER_HEAD', 'CREEPER_SPAWN_EGG', 'CREEPER_WALL_HEAD', 'CRIMSON_BUTTON',
    'CRIMSON_DOOR', 'CRIMSON_FENCE', 'CRIMSON_FENCE_GATE', 'CRIMSON_FUNGUS', 'CRIMSON_HYPHAE', 'CRIMSON_NYLIUM',
    'CRIMSON_PLANKS', 'CRIMSON_PRESSURE_PLATE', 'CRIMSON_ROOTS', 'CRIMSON_SIGN', 'CRIMSON_SLAB', 'CRIMSON_STAIRS',
    'CRIMSON_STEM', 'CRIMSON_TRAPDOOR', 'CROSSBOW', 'CRYING_OBSIDIAN', 'CUT_COPPER', 'CUT_COPPER_SLAB',
    'CUT_COPPER_STAIRS', 'CUT_RED_SANDSTONE', 'CUT_RED_SANDSTONE_SLAB', 'CUT_SANDSTONE', 'CUT_SANDSTONE_SLAB',
    'CYAN_BANNER', 'CYAN_BED', 'CYAN_CANDLE', 'CYAN_CARPET', 'CYAN_CONCRETE', 'CYAN_CONCRETE_POWDER',
    'YELLOW_TERRACOTTA', 'YELLOW_WOOL', 'ZOMBIE_HEAD', 'ZOMBIE_HORSE_SPAWN_EGG', 'ZOMBIE_SPAWN_EGG',
    'ZOMBIE_VILLAGER_SPAWN_EGG', 'ZOMBIFIED_PIGLIN_SPAWN_EGG'
]

# List of valid buttons from the Spigot API
BUTTONS = [
    'ACACIA_BUTTON', 'BIRCH_BUTTON', 'DARK_OAK_BUTTON', 'JUNGLE_BUTTON', 'OAK_BUTTON', 'SPRUCE_BUTTON', 'STONE_BUTTON'
]

# List of toowner options
TOOWNER_OPTIONS = ['true', 'false']


@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        height = int(request.form["height"])
        width = int(request.form["width"])
        portal_open = request.form["portal-open"]
        portal_closed = request.form["portal-closed"]
        button = request.form["button"]
        toowner = request.form["toowner"]

        return render_template("portal_grid.html", height=height, width=width, materials=MATERIALS,
                               portal_open=portal_open,
                               portal_closed=portal_closed, button=button, toowner=toowner)
    return render_template("index.html", materials=MATERIALS, buttons=BUTTONS, toowner_options=TOOWNER_OPTIONS)


@app.route("/generate", methods=["POST"])
def generate():
    height = int(request.form["height"])
    width = int(request.form["width"])
    portal_name = request.form["portal_name"]
    portal_open = request.form["portal-open"]
    portal_closed = request.form["portal-closed"]
    button = request.form["button"]
    toowner = request.form["toowner"]

    grid = []
    for i in range(height):
        row = []
        for j in range(width):
            row.append(request.form[f"cell-{i}-{j}"])
        grid.append(row)

    # Prepare portal file content
    portal_data = [
        f"portal-open={portal_open}",
        f"portal-closed={portal_closed}",
        f"button={button}",
        f"toowner={toowner}",
    ]

    for row in grid:
        portal_data.append("".join(row))

    # Save the file
    filename = f"{portal_name}.portal"
    filepath = os.path.join("portals", filename)

    os.makedirs("portals", exist_ok=True)
    with open(filepath, "w") as f:
        f.write("\n".join(portal_data))

    # Return the file for download
    return send_file(filepath, as_attachment=True)

if __name__ == "__main__":
    serve(app, host="0.0.0.0", port=8080)

