
import os
import importlib
import inspect
from pathlib import Path
from cmc.llm_classifier import add_entity_to_model
from cmc.model_post_processor import MentalModelPostProcessor

# Path to the mental model to update
MODEL_PATH = "data/systems_model.json"
SYSTEM_CONTEXT = "IT Organization"

# Dynamically import all loader modules from cmc.ingest
def discover_loaders():
    loader_dir = Path("cmc/ingest")
    loader_modules = []

    for file in loader_dir.glob("*_loader.py"):
        module_name = f"cmc.ingest.{file.stem}"
        module = importlib.import_module(module_name)
        loader_modules.append(module)

    return loader_modules

def run_ingestion_pipeline():
    print("🔍 Discovering loaders...")
    loaders = discover_loaders()

    for module in loaders:
        for name, obj in inspect.getmembers(module):
            if inspect.isclass(obj) and name.endswith("Loader"):
                print(f"📥 Running loader: {name}")
                loader_instance = obj()
                entities = loader_instance.load()
                for entity in entities:
                    add_entity_to_model(entity, MODEL_PATH, context=SYSTEM_CONTEXT)

    print(f"✅ All data ingested and classified into {MODEL_PATH}")
    
processor = MentalModelPostProcessor()
output_path = processor.post_process_and_save()
print(f"📦 Post-processed mental model saved to: {output_path}")

if __name__ == "__main__":
    run_ingestion_pipeline()
