//
//  AppState.swift
//  ReceiptTracker
//
//  Created by Yu Yun Liu on 2023-08-16.
//

import SwiftUI

struct AppStateData: Codable {
    var receipts: [Receipt] = []
    var searchResult: [Receipt] = []
}

@MainActor
class AppState: ObservableObject {
    /**
     this is the class that contains the state of the app
     there is only one instance of this class (singleton) and thus there will only one single source of truth throughout the entire application
     
     we only call the api service in the app state - the app state talks to the api and the views talk to the app state
     */
    @Published var store: AppStateData = AppStateData()
    
    func load() async throws {
        // call the service that loads the receipts from db
        APIService.shared.fetchReceipts(completion: { result in
            
            switch result {
            case .success(let receipts):
                DispatchQueue.main.async {
                    self.store.receipts = receipts
                }
            case .failure(let error):
                print("Error fetching receipts: \(error)")
            }
        })
    }
    
    func saveReceipt(receipt: Receipt) {
        self.store.receipts.append(receipt)
        APIService.shared.saveReceipt(receipt: receipt)
    }
    
    func search(search_str: String) {
        APIService.shared.fetchSearchResult(searchStr: search_str, completion: { search_result in
            switch search_result {
            case .success(let receipts):
                DispatchQueue.main.async {
                    self.store.searchResult = receipts
                }
            case .failure(let error):
                print("Error fetching receit: \(error)")
            }
        })
    }
    
    func clearSearch() {
        store.searchResult = []
    }
}
