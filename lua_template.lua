workshopItems = {{ 
{item_list}
}}

for _, steamId in pairs(workshopItems) do
    resource.AddWorkshop( tostring(steamId) )
end