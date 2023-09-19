//
//  SearchView.swift
//  ReceiptTracker
//
//  Created by Yu Yun Liu on 2023-09-02.
//

import SwiftUI

struct SearchView: View {
    @State private var searchString: String = ""
    @EnvironmentObject var appState: AppState
    
    var body: some View {
        VStack {
            if appState.store.searchResult.count > 0 {
                List($appState.store.searchResult) { $receipt in
                    NavigationLink(destination: ReceiptView(receipt: $receipt)) {
                        Text(receipt.id.uuidString)
                    }

                }
            }
            else {
                Text("No receipt match")
            }
        }
        .toolbar() {
            TextField("Search for a receipt", text: $searchString)
                .padding(7)
                .background(Color(.systemGray5))
                .cornerRadius(8)
                .padding(.horizontal, 10)
                .onChange(of: searchString) { newSearch in
                    appState.search(search_str: newSearch)
                }
        }
        .onDisappear() {
            appState.clearSearch()
            searchString = ""
        }
    }
}
