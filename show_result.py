import os
import json

def get_result(action_space, use_model, observation_type, corruption_type, result_dir):
    target_dir = os.path.join(result_dir, action_space, observation_type, corruption_type, use_model)
    if not os.path.exists(target_dir):
        print("New experiment, no result yet.")
        return None

    all_result = []
    domain_result = {}
    domain_instruction = {}
    filter_domain = {}
    all_result_for_analysis = {}
    
    for domain in os.listdir(target_dir):
        domain_path = os.path.join(target_dir, domain)
        if os.path.isdir(domain_path):
            for example_id in os.listdir(domain_path):
                example_path = os.path.join(domain_path, example_id)
                if os.path.isdir(example_path):
                    if "result.txt" in os.listdir(example_path):
                        # empty all files under example_id
                        if domain not in domain_result:
                            domain_result[domain] = []
                            filter_domain[domain] = []
                        result = open(os.path.join(example_path, "result.txt"), "r").read()
                        if int(eval(result)) == 1:
                            if domain not in domain_instruction:
                                domain_instruction[domain] = []
                            original_file = os.path.join('evaluation_examples/examples', domain, f'{example_id}.json')
                            with open(original_file, 'r') as file:
                                config_data = json.load(file)
                            instruction = config_data['instruction']

                            domain_instruction[domain].append({
                                'id': example_id,
                                'instruction': instruction
                            })
                            filter_domain[domain].append(example_id)
                        try:
                            domain_result[domain].append(float(result))
                        except:
                            domain_result[domain].append(float(eval(result)))

                        if domain not in all_result_for_analysis:
                            all_result_for_analysis[domain] = {}
                        all_result_for_analysis[domain][example_id] = domain_result[domain][-1]

                        try:
                            result = open(os.path.join(example_path, "result.txt"), "r").read()
                            try:
                                all_result.append(float(result))
                            except:
                                all_result.append(float(bool(result)))
                        except:
                            all_result.append(0.0)
    
    with open('evaluation_examples/filter_all.json', 'w') as file:
        json.dump(domain_instruction, file, indent=4)
    with open('evaluation_examples/filter_task.json', 'w') as file:
        json.dump(filter_domain, file, indent=4)
    
    total_success_num = 0

    for domain in domain_result:
        print("Domain:", domain, "Runned:", len(domain_result[domain]), "Success Rate:",
              sum(domain_result[domain]) / len(domain_result[domain]) * 100, "%")
        total_success_num += sum(domain_result[domain])
    
    print("total_success_num:", total_success_num)

    print(">>>>>>>>>>>>>")
    print("Office", "Success Rate:", sum(
        domain_result["libreoffice_calc"] + domain_result["libreoffice_impress"] + domain_result[
            "libreoffice_writer"]) / len(
        domain_result["libreoffice_calc"] + domain_result["libreoffice_impress"] + domain_result[
            "libreoffice_writer"]) * 100, "%")
    print("Daily", "Success Rate:",
          sum(domain_result["vlc"] + domain_result["thunderbird"] + domain_result["chrome"]) / len(
              domain_result["vlc"] + domain_result["thunderbird"] + domain_result["chrome"]) * 100, "%")
    print("Professional", "Success Rate:", sum(domain_result["gimp"] + domain_result["vs_code"]) / len(
        domain_result["gimp"] + domain_result["vs_code"]) * 100, "%")

    with open(os.path.join(target_dir, "all_result.json"), "w") as f:
        f.write(str(all_result_for_analysis))

    if not all_result:
        print("New experiment, no result yet.")
        return None
    else:
        print("Runned:", len(all_result), "Current Success Rate:", sum(all_result) / len(all_result) * 100, "%")
        return all_result


if __name__ == '__main__':
    get_result("pyautogui", "ui-tars", "screenshot", 'marks', "./results")
