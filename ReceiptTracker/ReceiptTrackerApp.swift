//
//  ReceiptTrackerApp.swift
//  ReceiptTracker
//
//  Created by Yu Yun Liu on 2023-07-22.
//

import SwiftUI

@main
struct ReceiptTrackerApp: App {
    
    @StateObject private var appState = AppState()
    var body: some Scene {
        WindowGroup {
            ContentView()
                .environmentObject(appState)
                .task {
                    do {
                        try await appState.load()
                    }
                    catch {
                        print("error loading app state: \(error)")
                    }
                }
        }
    }
}
