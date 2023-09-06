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
            Text("search view")
            
            if let t = appState.store.receipts[4].content {
                Text(t)
            }
            else {
                Text("no receipt text")
            }
        }
        .toolbar() {
            TextField("Search for a receipt", text: $searchString)
            
        }
    }
}
