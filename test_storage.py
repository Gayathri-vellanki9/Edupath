from edupath_storage import (
    save_results,
    load_results,
    results_exist
)


test_data = {
    "status": "success",
    "target_role": "Product Manager",
    "progress": 50,
    "skills": [
        "Product Management",
        "SQL"
    ]
}


print("\nSaving results...")

save_results(test_data)

print("Results saved:", results_exist())


print("\nLoading results...")

loaded_data = load_results()

print(loaded_data)


print("\nStorage test complete.")