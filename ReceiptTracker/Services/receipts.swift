//
//  receipts.swift
//  ReceiptTracker
//
//  Created by Yu Yun Liu on 2023-08-16.
//

import Foundation

class APIService {
    
    static func fetchReceipts(completion: @escaping (Result<[Receipt], Error>) -> Void) {
        guard let url = URL(string: "http://192.168.2.18:8000/receipts") else {
            return
        }
        
        URLSession.shared.dataTask(with: url) { data, response, error in
            if let error = error {
                completion(.failure(error))
                print("error in deconding data")
                return
            }
            
            if let data = data {
                do {
                    let receipts = try JSONDecoder().decode([Receipt].self, from: data)
                    completion(.success(receipts))
                }
                catch {
                    completion(.failure(error))
                }
            }
        }.resume()
    }
}
