from config.config_reader import CAR_FILTER_MAKE, CAR_FILTER_MODEL

def filterListings(listings):
    filteredListings = []

    for listing in listings:
        # Other fields validated in scraper service

        # Make filter
        model = listing.get('make')
        if model not in CAR_FILTER_MAKE:
            continue


        # Model filter
        model = listing.get('model')
        if model not in CAR_FILTER_MODEL:
            continue

        # Passed all filters
        filteredListings.append(listing)

    return filteredListings