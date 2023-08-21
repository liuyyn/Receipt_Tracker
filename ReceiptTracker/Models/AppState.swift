//
//  AppState.swift
//  ReceiptTracker
//
//  Created by Yu Yun Liu on 2023-08-16.
//

import SwiftUI

@MainActor
class AppState: ObservableObject {
    /**
     this is the class that contains the state of the app
     there is only one instance of this class (singleton) and thus there will only one single source of truth throughout the entire application
     */
    
    @Published var receipts: [Receipt] = []
    private var api = APIService()
    
    func load() async throws {
        // call the service that loads the receipts from db
        APIService.fetchReceipts(completion: { result in
            
            switch result {
            case .success(let receipts):
                DispatchQueue.main.async {
                    self.receipts = receipts
                    print("self.receipt = \(self.receipts)")
                }
            case .failure(let error):
                print("Error fetching receipts: \(error)")
            }
        })
    }
}
