import argparse
import pandas as pd
import pickle
import requests
from functools import partial
from multiprocessing import Pool
from tqdm import tqdm
import json

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--wit_entries_path', type=str)
    parser.add_argument('--output_path', type=str)
    parser.add_argument("--lang", type=str)
    parser.add_argument("--sample_factor", type=float, default=1)
    parser.add_argument("--nb_processes", type=int, default=1)
    parser.add_argument("--download_dict_path", type=str, default="")
    parser.add_argument("--caption_path", type=str)

    args = parser.parse_args()

    wit_entries_path = args.wit_entries_path
    output_path = args.output_path
    lang = args.lang
    sample_factor = args.sample_factor
    nb_processes = args.nb_processes
    download_dict_path = args.download_dict_path
    caption_path = args.caption_path

    headers = {
    'User-Agent':'Googlebot-Image/1.0',  # Pretend to be googlebot
    'X-Forwarded-For': '64.18.15.200'
    }

    if download_dict_path != "":
        with open(download_dict_path, 'rb') as handle:
            download_dict = pickle.load(handle)

    else:
        lang_entries = pd.read_pickle(wit_entries_path + "/{l}_entries.pkl".format(l = lang))
        print("Loaded {n} entries from {l}_entries.pkl.".format(n = len(lang_entries), l = lang))

        # filtering entries with caption
        lang_entries_with_captions = lang_entries[lang_entries.caption_reference_description.notna()]

        print("-> {n} entries with captions.".format(n = len(lang_entries_with_captions)))    

        # filtering entries in jpg or png format
        lang_entries_download = lang_entries_with_captions[~lang_entries_with_captions.image_url.str.endswith(".gif") & 
                                                   ~lang_entries_with_captions.image_url.str.endswith(".GIF") & 
                                                   ~lang_entries_with_captions.image_url.str.endswith(".svg") & 
                                                   ~lang_entries_with_captions.image_url.str.endswith(".SVG") &
                                                   ~lang_entries_with_captions.image_url.str.endswith(".webp")]

        print("-> {n} entries in png/jpg formats.".format(n = len(lang_entries_download))) 

        if sample_factor != 1:
            lang_entries_download = lang_entries_download.sample(frac=sample_factor, replace=False, random_state=1)

        print("-> {n} entries will be downloaded (after sampling).".format(n = len(lang_entries_download))) 

        lang_entries_filtered = lang_entries_download.drop([
                                     "hierarchical_section_title", 
                                     "caption_attribution_description",
                                     "caption_alt_text_description",
                                     "is_main_image",
                                     "attribution_passes_lang_id",
                                     "page_changed_recently",
                                     "context_page_description",
                                     "context_section_description"], 
                                     axis = 1)

        lang_entries_filtered["status"] = 0
        download_dict = lang_entries_filtered.to_dict("index")

        if download_dict_path == "":
            with open('download_dict_{l}_images.pickle'.format(l = lang), 'wb') as handle:
                pickle.dump(download_dict, handle, protocol=pickle.HIGHEST_PROTOCOL)

    download_list = list(download_dict.items())


    def download_image(pair, path_to_image_folder):

        index = pair[0]
        entry = pair[1]

        # image was already processed
        if entry["status"] != 0:
            return pair

        url = entry["image_url"]
        try:
            for agent in ['Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36', 'Googlebot-Image/1.0']:
                headers['User-Agent'] = agent
                response = requests.get(url, stream=False, timeout=60, allow_redirects=True, headers=headers)
                if response.ok:
                    break
            entry['status'] = response.status_code
        except Exception as e:
            # log errors later, set error as 408 timeout
            entry['status'] = 408
            return pair

        if response.ok:
            try:
                with open(path_to_image_folder + str(index), 'wb') as out_file:
                    # some sites respond with gzip transport encoding
                    response.raw.decode_content = True
                    out_file.write(response.content)
            except:
                # This is if it times out during a download or decode
                entry['status'] = 408
                return pair
        return pair

    def download_list_entries(list_entries, processes, path_to_image_folder, download_dict):
        pbar = tqdm(total=len(list_entries), position=0)

        with Pool(processes=processes) as pool:
            for pair in pool.imap_unordered(partial(download_image,
                                                    path_to_image_folder=path_to_image_folder
                                                    ), 
                                            list_entries):

                                index = pair[0]
                                entry = pair[1]
                                download_dict[index] = entry

                                pbar.update(1)
                                # saving dict for every 10k images downloaded
                                if (pbar.last_print_n % 10000) == 0:
                                    with open('download_dict_{l}_images.pickle'.format(l = lang), 'wb') as handle:
                                        pickle.dump(download_dict, handle, protocol=pickle.HIGHEST_PROTOCOL)



        pbar.close()


    download_list_entries(download_list, nb_processes, output_path + "/", download_dict)

    error_count = 0
    for pair in list(download_dict.items()):
        if pair[1]["status"] != 200:
            error_count += 1
    print("Encountered {e} errors while downloading the images.".format(e = error_count))

    download_list = list(download_dict.items())

    captions = {}
    for pair in download_list:

        index = pair[0]
        entry = pair[1]

        if entry["status"] == 200:
            captions[index] = entry["caption_reference_description"]

    # Saving captions
    with open(caption_path + "/{l}_captions.json".format(l = lang), "w", encoding="utf-8") as outfile:
        json.dump(captions, outfile, ensure_ascii=False)

    # Saving final download dict
    with open('download_dict_{l}_images.pickle'.format(l = lang), 'wb') as handle:
        pickle.dump(download_dict, handle, protocol=pickle.HIGHEST_PROTOCOL)